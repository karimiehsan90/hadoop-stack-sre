# hadoop:2.7.7

FROM openjdk:8u282

ARG REPOSITORY_URL=http://194.5.188.112:8080
ARG HADOOP_VERSION=2.7.7

ENV PATH=$PATH:/opt/hadoop/bin:/opt/hadoop/sbin \
    HADOOP_HOME=/opt/hadoop \
    HDFS_NAMENODE_USER="root" \
    HDFS_DATANODE_USER="root" \
    HDFS_SECONDARYNAMENODE_USER="root" \
    YARN_RESOURCEMANAGER_USER="root" \
    YARN_NODEMANAGER_USER="root" \
    HADOOP_REPLICATION="2" \
    HADOOP_NAMENODE_HOST="localhost" \
    HADOOP_NAMENODE_PORT="9000" \
    HADOOP_RESOURCEMANAGER_HOST="localhost"

COPY config/hdfs-site.xml config/core-site.xml config/yarn-site.xml config/mapred-site.xml /etc/hadoop-config/

COPY run.sh templater.sh /bin/

RUN apt update \
    && apt install -y --no-install-recommends curl \
    && curl -sL ${REPOSITORY_URL}/hadoop-${HADOOP_VERSION}.tar.gz -o /hadoop-${HADOOP_VERSION}.tar.gz \
    && tar -xvzf /hadoop-${HADOOP_VERSION}.tar.gz -C /opt \
    && rm /hadoop-${HADOOP_VERSION}.tar.gz \
    && mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop \
    && mkdir /var/lib/hadoop \
    && ln -s /opt/hadoop/etc/hadoop /etc/hadoop \
    && ln -s /opt/hadoop/logs /var/log/hadoop \
    && chmod +x /bin/run.sh /bin/templater.sh \
    && templater.sh \
    && hadoop namenode -format

WORKDIR /opt/hadoop

# HDFS ports
EXPOSE 50070 50470 8020 9000 50075

# YARN ports
EXPOSE 8088 8031 8032 8033

ENTRYPOINT ["run.sh"]
