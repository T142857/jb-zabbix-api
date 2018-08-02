import json
import sys
from zabbix_api import ZabbixAPI
import time
from datetime import datetime, timedelta
import pytz
import json

zx = ZabbixAPI(server="http://192.168.158.138")
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


def get_itemids_by_name(key=None):
    params = {'search': {
        "key_": key}, 'output': zx.QUERY_EXTEND}
    metrics = zx.call('item.get', params)
    for metric in metrics:
        print metric["itemid"]
        print metric["name"]
        # print json.dumps(metrics, indent=4, sort_keys=True)


def get_history_by_itemid(itemid, limit):
    params = {'history': 0, 'itemids': itemid, "sortfield": "clock", "sortorder": "DESC", "limit": limit,
              'output': zx.QUERY_EXTEND}
    metrics = zx.call('history.get', params)
    print json.dumps(metrics, indent=4, sort_keys=True)


def get_history_by_itemid_(itemid):
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    delta = timedelta(minutes=60)
    time_now = datetime.now(tz)
    time_delta = time_now - delta
    time_till = datetime_to_epoch(time_now)
    time_from = datetime_to_epoch(time_delta)
    params = {'history': 0, 'itemids': itemid, "sortfield": "clock", 'time_from': time_from, 'time_till': time_till,
              'output': zx.QUERY_EXTEND}
    metrics = zx.call('history.get', params)
    for e in metrics:
        del e['ns']
        del e['itemid']

    print json.dumps(metrics, indent=4, sort_keys=True)


def datetime_to_epoch(t):
    t = t.strftime('%y-%m-%d %H:%M:%S')
    date = time.strptime(t, "%y-%m-%d %H:%M:%S")
    return datetime.fromtimestamp(time.mktime(date)).strftime('%s')


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
    # key = sys.argv[1]
    # print(get_itemids_by_name(key))
    get_history_by_itemid_('28399')
