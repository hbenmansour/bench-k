FROM registry.access.redhat.com/rhel:7.4

ENV ZOOKEEPER=my-cluster-zookeeper:2181
ENV KAFKA=my-cluster-kafka:9092

RUN yum -y install java-1.8.0-openjdk-headless gettext nmap-ncat python && yum clean all -y

RUN groupadd -r -g 1001 benchmark && useradd -r -m -u 1001 -g benchmark benchmark

ADD  ./run_benchmark.py /home/benchmark/
ADD  ./run_benchmark.sh /home/benchmark/
USER benchmark

WORKDIR /home/benchmark/

ENTRYPOINT /run_benchmark.sh
