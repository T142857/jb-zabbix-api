import json
import sys
from zabbix_api import ZabbixAPI

zx = ZabbixAPI(server="http://172.25.32.5/zabbix")
zx.login('Admin', 'zabbix')


# users = zx.call('user.get', {'output': zx.QUERY_EXTEND})
# users = zx.user.get({'output': zx.QUERY_EXTEND})
# print users

# params = {'filter': {'host': ['fpt-compute01']}, 'output': zx.QUERY_EXTEND}
# dhost = zx.call('host.get', params)
# print dhost


def get_groupids(search=None):
    """
    Get the groupids by name
    :param str search 
    return groupids
    """
    if search is not None:
        params = {'search': {'name': [search]}, 'output': zx.QUERY_EXTEND}
    else:
        params = {'output': zx.QUERY_EXTEND}
    # print json.dumps(zx.call('hostgroup.get', params), indent=4, sort_keys=True)
    # return json.dumps(zx.call('hostgroup.get', params))
    groups = zx.call('hostgroup.get', params)
    groupids = []
    if groups is not None:
        for g in groups:
            groupids.append(g["groupid"])
    return groupids


def get_hostids_by_groupids(groupids=None):
    if groupids is not None:
        params = {'groupids': groupids, 'output': zx.QUERY_EXTEND}
    else:
        params = {'output': zx.QUERY_EXTEND}
    hosts = zx.call('host.get', params)
    hostids = []
    if hosts is not None:
        for h in hosts:
            hostids.append(h["hostid"])
    return hostids

    # print json.dumps(hosts, indent=4, sort_keys=True)


def get_hostids_by_name(search=None):
    pass


def host_get_items(hostids, key=None):
    if hostids is not None and key is not None:
        params = {'hostids': hostids, 'search': {
            "key_": key}, 'output': zx.QUERY_EXTEND}
    else:
        params = {'output': zx.QUERY_EXTEND}
    metrics = zx.call('item.get', params)
    # print json.dumps(metrics, indent=4, sort_keys=True)
    if metrics is not None:
        return summary_metrics(metrics)
    else:
        return 0


def summary_metrics(metrics):
    total = 0
    for metric in metrics:
        # print "metric: %s vaule: %s" % (metric["key_"], metric["lastvalue"])
        total = float(total) + float(metric["lastvalue"])
    return total


def progress(search, key):
    groupids = get_groupids(search=search)
    hostids = get_hostids_by_groupids(groupids)
    return host_get_items(hostids, key=key)


if __name__ == '__main__':

    search = sys.argv[1]
    key = sys.argv[2]
    if search and key:
        print progress(search, key)
