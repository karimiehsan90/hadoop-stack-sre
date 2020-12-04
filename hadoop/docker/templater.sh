#!/usr/bin/env bash

set -euo pipefail

cp /etc/hadoop-config/* /etc/hadoop
sed -i "s/HADOOP_REPLICATION/${HADOOP_REPLICATION}/" /etc/hadoop/hdfs-site.xml
sed -i "s/HADOOP_NAMENODE_HOST/${HADOOP_NAMENODE_HOST}/" /etc/hadoop/core-site.xml
sed -i "s/HADOOP_NAMENODE_PORT/${HADOOP_NAMENODE_PORT}/" /etc/hadoop/core-site.xml
sed -i "s/HADOOP_RESOURCEMANAGER_HOST/${HADOOP_RESOURCEMANAGER_HOST}/" /etc/hadoop/yarn-site.xml
