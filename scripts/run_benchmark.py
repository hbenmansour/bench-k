import os
import subprocess
import argparse
import json
import threading
from concurrent.futures import ThreadPoolExecutor, wait, as_completed

KAFKA_PATH="/opt/kafka/"
N_MSG=200000
MSG_SIZE=200
TOPIC="bench01"
REPLICATION=3
N_PARTITIONS=10
THROUGHPUT=18000
ACK="None"
N_CONSUMERS=1
N_PRODUCERS=1
N_ITER=10

parser = argparse.ArgumentParser()
parser.add_argument("-z","--zookeeper", help="address of the zookeeper cluster",required=True)
parser.add_argument("-k","--kafka", help="address of the kafka broker",required=True)
parser.add_argument("-p","--path", help="path for kafka binaries",default=KAFKA_PATH)
parser.add_argument("-n","--nmsg", help="number of messages",type=int,default=N_MSG)
parser.add_argument("-s","--msgsize", help="size of messages",type=int,default=MSG_SIZE)
parser.add_argument("-t","--topic", help="topic to be used",default=TOPIC)
parser.add_argument("-r","--replication", help="replication factor",type=int,default=REPLICATION)
parser.add_argument("-npt","--npartitions", help="number of partitions",type=int,default=N_PARTITIONS)
parser.add_argument("-th","--throughput", help="throughput",type=int,default=THROUGHPUT)
parser.add_argument("-a","--ack", help="ack strategy to be used",default=ACK,choices=["None","Leader","All"])
parser.add_argument("-nc","--nconsumers", help="number of consumers",type=int,default=N_CONSUMERS)
parser.add_argument("-np","--nproducers", help="number of producers",type=int,default=N_PRODUCERS)
parser.add_argument("-f","--file", help="file where to store metrics",default=None)
parser.add_argument("-v","--verbose", help="whether or not it should print verbose logging messages",type=bool,default=True)
#parser.add_argument("-re","--config ", help="What's the retention config in ms for the topic",default=TOPIC_CONFIG)
args = parser.parse_args()

if args.verbose:
    print "Running script with parameters:", args

kafka_bin = os.path.join(args.path, "bin")
kafka_topic_bin = os.path.join(kafka_bin, "kafka-topics.sh")
kafka_producer_bin = os.path.join(kafka_bin, "kafka-producer-perf-test.sh")
kafka_consumer_bin = os.path.join(kafka_bin, "kafka-consumer-perf-test.sh")

producer_metrics = {}
consumer_metrics = {}

ack = None
if args.ack == "None":
    ack = "0"
elif args.ack == "Leader":
    ack = "1"
else:
    ack = "2"

class Producer(threading.Thread):
    def __init__(self, pid):
        self.pid = pid
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        if args.verbose:
                print "Launching producer #"+str(self.pid)
        output = subprocess.check_output([kafka_producer_bin,"--topic",args.topic,"--num-records",str(args.nmsg),"--record-size",str(args.msgsize),
        "--throughput",str(args.throughput),"--producer-props","acks="+ack,"bootstrap.servers="+args.kafka,"--print-metrics"])
        if args.verbose:
                print "Output: "+output
        if args.verbose:
                print "Producer #"+str(self.pid)+" is done"

        lines = output.split("\n")
        for line in lines:
                if not line.startswith("producer-metrics:"):
                        continue
                data = line.split(":")
                metric = data[1].strip()
                value = None
                try:
                        value = float(data[-1].strip())
                except:
                        value = 0
                if metric not in producer_metrics:
                        producer_metrics[metric] = []
                producer_metrics[metric].append(value)

for i in range(N_ITER):
    if args.verbose:
        print "Iteration #"+str(i)
	print "Parameter inside the iteration:", args
    

    pool = ThreadPoolExecutor(args.nconsumers)
    future = pool.submit(subprocess.check_output([kafka_consumer_bin,"--topic",args.topic,"--broker-list",args.kafka,"--messages",str(args.nmsg),"--threads",str(args.nconsumers),
    "--num-fetch-threads",str(args.nconsumers),"--print-metrics"]))

    if args.verbose:
    	print "The Topic should be created by the topic controller"
#    	print "Creating topic"
# 	exitcode = subprocess.check_call(
#      	[kafka_topic_bin, "--zookeeper", args.zookeeper, "--create", "--topic", args.topic, "--replication-factor", str(args.replication), "--partitions", str(args.npartitions), " --config TOPIC_CONFIG", str(args.config)])
#    	[kafka_topic_bin, "--zookeeper", args.zookeeper, "--create", "--topic", args.topic, "--replication-factor", str(args.replication), "--partitions", str(args.npartitions)])
# 	if exitcode != 0:
#      	raise Exception("Error creating topic")
#   	if args.verbose:
        print "Created topic"

    if args.verbose:
        print "Running producer tasks"
    tasks = []
    for j in range(args.nproducers):
        tasks.append(Producer(j))
    for t in tasks:
        t.start()
    if args.verbose:
        print "Waiting all producer tasks to be done"
    for t in tasks:
        t.join()
    if args.verbose:
        print "All producer tasks are done"

    if args.verbose:
        print "Launching consumer"
    #output = subprocess.check_output([kafka_consumer_bin,"--topic",args.topic,"--broker-list",args.kafka,"--messages",str(args.nmsg),"--threads",str(args.nconsumers),
    #"--num-fetch-threads",str(args.nconsumers),"--print-metrics"])
    for f in concurrent.futures.as_completed(future)
        output = f.result()
        print "Consumer is done"
        lines = output.split("\n")
        for line in lines:
            if not line.startswith("consumer-"):
                    continue
            data = line.split(":")
            metric = data[1].strip()
            value = None
            try:
                    value = float(data[-1].strip())
            except:
                    value = 0
            if metric not in consumer_metrics:
                    consumer_metrics[metric] = []
            consumer_metrics[metric].append(value)

    if args.verbose:
	print "Make sure the Topic controller deletes the topic"
#        print "Deleting topic"
#    exitcode = subprocess.check_call([kafka_topic_bin, "--zookeeper", args.zookeeper, "--delete", "--topic", args.topic])
#    if exitcode != 0:
#        raise Exception("Error deleting topic")
#    if args.verbose:
#        print "Deleted topic"

if args.file is not None:
        if args.verbose:
                print "Writing metrics to file: "+args.file
        with open(args.file,"w") as outputfile:
                metricsdata = {"consumer":{},"producer":{}}
                for metric in consumer_metrics:
                        metricsdata["consumer"][metric] = float(sum(consumer_metrics[metric])) / float(len(consumer_metrics[metric]))
                for metric in producer_metrics:
                        metricsdata["producer"][metric] = float(sum(producer_metrics[metric])) / float(len(producer_metrics[metric]))
                outputfile.write(json.dumps(metricsdata,indent=4))

if args.verbose:
    print "Benchmark is done!"
