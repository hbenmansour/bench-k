#!/bin/bash

#python run_benchmark.py -z my-cluster-zookeeper:2181 -k my-cluster-kafka:9092
#python run_benchmark.py -z my-cluster-zookeeper:2181 -k my-cluster-kafka:9092 -t $TOPIC -n $N_MSG  -s $MSG_SIZE -npt $N_PARTITIONS -nc $N_CONSUMERS -np $N_PRODUCERS -r $REPLICATION -a $ACK -th $THROUGHPUT
python run_benchmark.py -z my-cluster-zookeeper-headless:2181 -k my-cluster-kafka-headless:9092 -t $TOPIC -n $N_MSG  -s $MSG_SIZE -npt $N_PARTITIONS -nc $N_CONSUMERS -np $N_PRODUCERS -r $REPLICATION -a $ACK -th $THROUGHPUT
