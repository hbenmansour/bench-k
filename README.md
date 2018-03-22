# Kafka benchmark

This repository contain dockerfile to build an image to perform benchmark on Kafka. 

This image is intended to be use in an OpenShift cluster in the same project as the Kafka cluster.

A yaml template is provided to facilitate usage of this image as a job.


## Build the test image

To luanch a s2i build in order to build the image inside openshift cluster and have it in internal registry in current namespace : 
```
oc new-build https://github.com/jihed/bench-k.git
```


## Create template 

To create in current namespace a template for kafka benchmark job creation 
```
oc create -f template-job.yml
```


## Launch benchmark

To launch kafka benchmark with default value run 
```
oc new-app job-kafka-bench
```

## Available parameters : 



| NAME               | DESCRIPTION                     | GENERATOR         |  VALUE |
| ------------------ | ------------------------------- | ----------------- | ----------------------------------------------- |
| JOB_NAME           |  Job name                       |                   |   job-kafka-bench |
| JOB_IMAGE          |  Job image                      |                   |   172.30.203.45:5000/strimzi-0201/bench-k:latest |
| PARAM_TOPIC        |  Bench parameter - Topic        |                   |   mybench |
| PARAM_THROUGHPUT   |  Bench parameter - THROUGHPUT   |                   |   1000 |
| PARAM_REPLICATION  |  Bench parameter - REPLICATION  |                   |   1 |
| PARAM_N_PRODUCERS  |  Bench parameter - N_PRODUCERS  |                   |   1 |
| PARAM_N_PARTITIONS |  Bench parameter - N_PARTITIONS |                   |   1 |
| PARAM_N_MSG        |  Bench parameter - N_MSG        |                   |   1000 |
| PARAM_N_ITER       |  Bench parameter - N_ITER       |                   |   1 |
| PARAM_N_CONSUMERS  |  Bench parameter - N_CONSUMERS  |                   |   1 |
| PARAM_MSG_SIZE     |  Bench parameter - MSG_SIZE     |                   |   100 |
| PARAM_ACK          | Bench parameter - ACK           |                   |  None |


Run a job with customized parameter : 
```
oc new-app job-kafka-bench -p JOB_NAME=mybenchtest -p PARAM_TOPIC=mytopic
```

PS Update the image repo according to your repo/project.
```

