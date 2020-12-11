import os
import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from collector.namenode import NameNodeCollector


NAMENODE_HOST = os.getenv('NAMENODE_HOST', 'localhost')
NAMENODE_UI_PORT = int(os.getenv('NAMENODE_UI_PORT', '50070'))
EXPORTER_PORT = int(os.getenv('HADOOP_EXPORTER_PORT', '9091'))


def main():
    namenode_collector = NameNodeCollector(NAMENODE_HOST, NAMENODE_UI_PORT)
    REGISTRY.register(namenode_collector)
    start_http_server(EXPORTER_PORT)
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
