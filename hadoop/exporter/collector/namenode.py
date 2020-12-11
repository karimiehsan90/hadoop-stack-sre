import requests
import json
from prometheus_client.core import GaugeMetricFamily


class NameNodeCollector:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.jvm_metrics = {}
        self.namenode_metrics = {}
        self.datanode_metrics = {}
        self.jvm_statuses = {
            'MemNonHeapUsedM': {
                'prometheus': 'mem_non_heap_used_m',
                'documentation': 'Non heap used memory'
            },
            'MemNonHeapCommittedM': {
                'prometheus': 'mem_non_heap_committed_m',
                'documentation': 'Non heap committed memory'
            },
            'MemNonHeapMaxM': {
                'prometheus': 'mem_non_heap_max_m',
                'documentation': 'Non heap used max memory'
            },
            'MemHeapUsedM': {
                'prometheus': 'mem_heap_used_m',
                'documentation': 'Heap used memory'
            },
            'MemHeapCommittedM': {
                'prometheus': 'mem_heap_committed_m',
                'documentation': 'Heap committed memory'
            },
            'MemHeapMaxM': {
                'prometheus': 'mem_heap_max_m',
                'documentation': 'Heap max memory'
            },
            'MemMaxM': {
                'prometheus': 'mem_max_m',
                'documentation': 'Max Memory'
            },
            'GcCount': {
                'prometheus': 'gc_count',
                'documentation': 'GC count'
            },
            'GcTimeMillis': {
                'prometheus': 'gc_time_millis',
                'documentation': 'GC time millis'
            },
            'GcNumWarnThresholdExceeded': {
                'prometheus': 'gc_number_warn_threshold_exceeded',
                'documentation': 'GC number warn threshold exceeded'
            },
            'GcNumInfoThresholdExceeded': {
                'prometheus': 'gc_number_info_threshold_exceeded',
                'documentation': 'GC number info threshold exceeded'
            },
            'GcTotalExtraSleepTime': {
                'prometheus': 'gc_total_extra_sleep_time',
                'documentation': 'GC total extra sleep time'
            },
            'ThreadsNew': {
                'prometheus': 'threads_new',
                'documentation': 'Threads in new state'
            },
            'ThreadsRunnable': {
                'prometheus': 'threads_runnable',
                'documentation': 'Threads in runnable state'
            },
            'ThreadsBlocked': {
                'prometheus': 'threads_blocked',
                'documentation': 'Threads in blocked state'
            },
            'ThreadsWaiting': {
                'prometheus': 'threads_waiting',
                'documentation': 'Threads in waiting state'
            },
            'ThreadsTimedWaiting': {
                'prometheus': 'threads_timed_waiting',
                'documentation': 'Threads in timed waiting state'
            },
            'ThreadsTerminated': {
                'prometheus': 'threads_terminated',
                'documentation': 'Threads in terminated state'
            },
            'LogFatal': {
                'prometheus': 'log_fatal',
                'documentation': 'Total fatal logs'
            },
            'LogError': {
                'prometheus': 'log_error',
                'documentation': 'Total error logs'
            }
        }
        self.namenode_statuses = {
            'CapacityTotal': {
                'prometheus': 'capacity_total',
                'documentation': 'Total capacity'
            },
            'CapacityUsed': {
                'prometheus': 'capacity_used',
                'documentation': 'Used capacity'
            },
            'CapacityRemaining': {
                'prometheus': 'capacity_remaining',
                'documentation': 'Remaining capacity'
            },
            'MissingBlocks': {
                'prometheus': 'missing_blocks',
                'documentation': 'Missing blocks'
            },
            'BlocksTotal': {
                'prometheus': 'blocks_total',
                'documentation': 'Total blocks'
            },
            'FilesTotal': {
                'prometheus': 'files_total',
                'documentation': 'Total files'
            },
            'PendingReplicationBlocks': {
                'prometheus': 'pending_replication_blocks',
                'documentation': 'Pending replication blocks'
            },
            'UnderReplicatedBlocks': {
                'prometheus': 'under_replicated_blocks',
                'documentation': 'Under replicated blocks'
            },
            'ScheduledReplicationBlocks': {
                'prometheus': 'scheduled_replication_blocks',
                'documentation': 'Scheduled replication blocks'
            },
            'PendingDeletionBlocks': {
                'prometheus': 'pending_deletion_blocks',
                'documentation': 'Pending deletion blocks'
            },
            'NumLiveDataNodes': {
                'prometheus': 'live_datanodes',
                'documentation': 'Live datanodes'
            },
            'NumDecomLiveDataNodes': {
                'prometheus': 'live_decommission_datanodes',
                'documentation': 'Live decommission datanodes'
            },
            'NumDecomDeadDataNodes': {
                'prometheus': 'dead_decommission_datanodes',
                'documentation': 'Dead decommission datanodes'
            },
            'NumDecommissioningDataNodes': {
                'prometheus': 'total_decommission_datanodes',
                'documentation': 'Total decommission datanodes'
            },
            'VolumeFailuresTotal': {
                'prometheus': 'volume_failures_total',
                'documentation': 'Volume failure total'
            },
            'EstimatedCapacityLostTotal': {
                'prometheus': 'estimated_capacity_lost',
                'documentation': 'Estimated capacity lost'
            },
            'PostponedMisreplicatedBlocks': {
                'prometheus': 'postponed_misreplicated_blocks',
                'documentation': 'Postponed MisReplicated blocks'
            }
        }

    def collect(self):
        self.initialize_metrics()
        beans = self.get_beans()
        self.get_metrics(beans)
        for key, metric in self.jvm_metrics.items():
            yield metric
        for key, metric in self.namenode_metrics.items():
            yield metric
        yield self.datanode_metrics['status']

    def initialize_metrics(self):
        for status, value in self.jvm_statuses.items():
            self.jvm_metrics[status] = GaugeMetricFamily('hadoop_jvm_{}'.format(value['prometheus']),
                                                         labels=['process_name', 'hostname'],
                                                         documentation=value['documentation'])
        for status, value in self.namenode_statuses.items():
            self.namenode_metrics[status] = GaugeMetricFamily('hadoop_namenode_{}'.format(value['prometheus']),
                                                              labels=['state', 'hostname'],
                                                              documentation=value['documentation'])
        self.datanode_metrics['status'] = GaugeMetricFamily('hadoop_datanode_status', labels=['host'],
                                                            documentation='Datanode state live=1 dead=2 decom=3')

    def get_metrics(self, beans):
        for bean in beans:
            if bean['name'] == 'Hadoop:service=NameNode,name=JvmMetrics':
                for status, value in self.jvm_statuses.items():
                    self.jvm_metrics[status].add_metric(value=bean.get(status), labels=[bean.get('tag.ProcessName'),
                                                                                        bean.get('tag.Hostname')])
            elif bean['name'] == 'Hadoop:service=NameNode,name=FSNamesystem':
                for status, value in self.namenode_statuses.items():
                    self.namenode_metrics[status].add_metric(value=bean.get(status), labels=[bean.get('tag.HAState'),
                                                                                             bean.get('tag.Hostname')])
            elif bean['name'] == 'Hadoop:service=NameNode,name=NameNodeInfo':
                live_nodes = json.loads(bean['LiveNodes'])
                dead_nodes = json.loads(bean['DeadNodes'])
                decommission_nodes = json.loads(bean['DecomNodes'])
                for node, value in live_nodes.items():
                    self.datanode_metrics['status'].add_metric(value='1', labels=[node])
                for node, value in dead_nodes.items():
                    self.datanode_metrics['status'].add_metric(value='2', labels=[node])
                for node, value in decommission_nodes.items():
                    self.datanode_metrics['status'].add_metric(value='3', labels=[node])

    def get_beans(self):
        response = requests.get('http://{}:{}/jmx'.format(self.host, self.port))
        response_content = response.content.decode('utf-8')
        response_dict = json.loads(response_content)
        beans = response_dict['beans']
        return beans

