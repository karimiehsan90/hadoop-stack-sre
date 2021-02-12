#!/usr/bin/env bash

set -euo pipefail

templater.sh
if [ ${HADOOP_ROLE} == "datanode" ]; then
    SCRIPT=hdfs
    rm -rf /var/lib/hadoop/current
fi

if [ ${HADOOP_ROLE} == "namenode" ]; then
    SCRIPT=hdfs
fi

if [ ${HADOOP_ROLE} == "nodemanager" ]; then
    SCRIPT=yarn
    rm -rf /var/lib/hadoop/current
fi

if [ ${HADOOP_ROLE} == "resourcemanager" ]; then
    SCRIPT=yarn
    rm -rf /var/lib/hadoop/current
fi

${SCRIPT} "${HADOOP_ROLE}"
