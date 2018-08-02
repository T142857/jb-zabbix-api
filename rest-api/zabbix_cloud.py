import json
import sys
from zabbix_api import ZabbixAPI
import time
from datetime import datetime, timedelta
import pytz
import json
import os 

tz = pytz.timezone('Asia/Ho_Chi_Minh')
delta = timedelta(minutes=300)

zx = ZabbixAPI(server="%s/api_jsonrpc.php" % (os.getenv('ZABBIX_HOST')))
zx.login('%s' % os.getenv('ZABBIX_USER'), '%s' % os.getenv('ZABBIX_PASS'))


def datetime_to_epoch(t):
    t = t.strftime('%y-%m-%d %H:%M:%S')
    date = time.strptime(t, "%y-%m-%d %H:%M:%S")
    return datetime.fromtimestamp(time.mktime(date)).strftime('%s')


def metric_convert_name(name):
    # split_ = name.split(" - ")
    split_ = name.split("__")
    return split_[-1]


def get_metrics_by_uuid(uuid=None):
    """
    get all metrics by keyword
    """
    _metrics = []
    params = {'search': {"key_": uuid}, 'output': zx.QUERY_EXTEND}
    metrics = zx.call('item.get', params)
    for metric in metrics:
        _metrics.append(
            {'itemid': metric["itemid"], 'itemname': metric_convert_name(metric["name"])})
    print(json.dumps(_metrics, indent=4, sort_keys=True))
    return _metrics


def type_convert(k):
    """
    History object types to return.

    Possible values:
    0 - numeric float;
    1 - character;
    2 - log;
    3 - numeric unsigned;
    4 - text.

    Default: 3.
    """
    types = {'process_load': 0, 'ping': 3, 'service_api': 3}
    if k in types:
        return types[k]
    return None


def get_history_by_itemid(k, itemid):
    """
    get list metric data of item
    :param itemid: item id
    :return:
    """
    
    if itemid is None or type_convert(k) is None:
        return []

    time_now = datetime.now(tz)
    time_delta = time_now - delta
    time_till = datetime_to_epoch(time_now)
    time_from = datetime_to_epoch(time_delta)
    params = {'history': type_convert(k), 'itemids': itemid, "sortfield": "clock", 'time_from': time_from, 'time_till': time_till,
              'output': zx.QUERY_EXTEND}
    # print(params)
    metrics = zx.call('history.get', params)
    # print('ffff' + str(metrics))

    for e in metrics:
        if 'ns' in e and 'itemid' in e:
            del e['ns']
            del e['itemid']

    # print json.dumps(metrics, indent=4, sort_keys=True)
    return metrics


# def main():
#     # metrics = get_metrics_by_uuid('51362af0-e375-403e-a192-10dd56a58c25')
#     # print json.dumps(metrics, indent=4, sort_keys=True)
#     data = get_history_by_itemid('28625', 'ping')
#     print(data)


# if __name__ == '__main__':
#     main()
