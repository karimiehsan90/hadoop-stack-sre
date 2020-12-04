#!/usr/bin/env bash

set -euo pipefail

templater.sh
if [ ${HADOOP_ROLE} == "datanode" ]; then
    DAEMON_SCRIPT=hadoop
    rm -rf /var/lib/hadoop/current
fi

if [ ${HADOOP_ROLE} == "namenode" ]; then
    DAEMON_SCRIPT=hadoop
fi

if [ ${HADOOP_ROLE} == "nodemanager" ]; then
    DAEMON_SCRIPT=yarn
    rm -rf /var/lib/hadoop/current
fi

if [ ${HADOOP_ROLE} == "resourcemanager" ]; then
    DAEMON_SCRIPT=yarn
    rm -rf /var/lib/hadoop/current
fi

${DAEMON_SCRIPT}-daemon.sh start "${HADOOP_ROLE}"
HOSTNAME=$(hostname)
tail -f /var/log/hadoop/${DAEMON_SCRIPT}--${HADOOP_ROLE}-${HOSTNAME}.out --lines 1000
