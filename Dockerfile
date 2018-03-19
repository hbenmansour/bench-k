FROM registry.access.redhat.com/rhel:7.4

RUN yum -y install java-1.8.0-openjdk-headless gettext nmap-ncat hostname python && yum clean all -y

# set Kafka home folder
ENV KAFKA_HOME=/opt/kafka
# expose port kafka and zk 
EXPOSE 9092 2181


# Add kafka group / user
RUN groupadd -r -g 1001 kafka && useradd -r -m -u 1001 -g kafka kafka

# Set Scala and Kafka version
ENV SCALA_VERSION=2.12
ENV KAFKA_VERSION=1.0.1

# Set Kafka (SHA512) and Prometheus JMX exporter (SHA1) checksums
ENV KAFKA_CHECKSUM="935c0df1cf742405c40d9248cfdd1578038b595b59ec5a350543a7fe67b6be26ff6c4426f7c0c072ff4aa006b701502a55fcf7e2ced1fdc64330e3383035078c  kafka_2.12-1.0.1.tgz"

# Set from build args
ARG version=latest
ENV VERSION ${version}

# Downloading/extracting Apache Kafka
RUN curl -O https://www.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    && echo $KAFKA_CHECKSUM > kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz.sha512 \
    && sha512sum --check kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz.sha512 \
    && mkdir $KAFKA_HOME \
    && tar xvfz kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz -C $KAFKA_HOME --strip-components=1 \
    && rm -f kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz*

WORKDIR $KAFKA_HOME
COPY  ./scripts $KAFKA_HOME 

USER kafka:kafka

#CMD ["/opt/kafka/run_benchmark.sh"]
