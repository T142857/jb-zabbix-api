#!/usr/bin/env python
import urllib2
import json
import argparse


def authenticate(url, username, password):
    values = {'jsonrpc': '2.0',
              'method': 'user.login',
              'params': {
                  'user': username,
                  'password': password
              },
              'id': '0'
              }

    data = json.dumps(values)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
    response = urllib2.urlopen(req, data)
    output = json.loads(response.read())

    try:
        message = output['result']
    except:
        message = output['error']['data']
        print message
        quit()

    return output['result']


def getGraph(hostname, url, auth, graphtype, dynamic, columns):
    if (graphtype == 0):
        selecttype = ['graphid']
        select = 'selectGraphs'
    if (graphtype == 1):
        selecttype = ['itemid', 'value_type']
        select = 'selectItems'

    values = {'jsonrpc': '2.0',
              'method': 'host.get',
              'params': {
                  select: selecttype,
                  'output': ['hostid', 'host'],
                  'searchByAny': 1,
                  'filter': {
                      'host': hostname
                  }
              },
              'auth': auth,
              'id': '2'
              }

    data = json.dumps(values)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
    response = urllib2.urlopen(req, data)
    host_get = response.read()

    output = json.loads(host_get)
    # print json.dumps(output)

    graphs = []
    if (graphtype == 0):
        for i in output['result'][0]['graphs']:
            graphs.append(i['graphid'])

    if (graphtype == 1):
        for i in output['result'][0]['items']:
            if int(i['value_type']) in (0, 3):
                graphs.append(i['itemid'])

    graph_list = []
    x = 0
    y = 0

    for graph in graphs:
        graph_list.append({
            "resourcetype": graphtype,
            "resourceid": graph,
            "width": "500",
            "height": "100",
            "x": str(x),
            "y": str(y),
            "colspan": "1",
            "rowspan": "1",
            "elements": "0",
            "valign": "0",
            "halign": "0",
            "style": "0",
            "url": "",
            "dynamic": str(dynamic)
        })
        x += 1
        if x == columns:
            x = 0
            y += 1

    return graph_list


def screenCreate(url, auth, screen_name, graphids, columns):
    # print graphids
    if len(graphids) % columns == 0:
        vsize = len(graphids) / columns
    else:
        vsize = (len(graphids) / columns) + 1

    values = {"jsonrpc": "2.0",
              "method": "screen.create",
              "params": [{
                  "name": screen_name,
                  "hsize": columns,
                  "vsize": vsize,
                  "screenitems": []
              }],
              "auth": auth,
              "id": 2
              }

    for i in graphids:
        values['params'][0]['screenitems'].append(i)

    data = json.dumps(values)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
    response = urllib2.urlopen(req, data)
    host_get = response.read()

    output = json.loads(host_get)

    try:
        message = output['result']
    except:
        message = output['error']['data']

    print json.dumps(message)


def host_get(url, auth, hostids):
    # values = {
    #     "jsonrpc": "2.0",
    #     "method": "host.get",
    #     "params": {
    #         "output": "extend",
    #         "filter": {
    #             "host": [
    #                 "fpt-compute01",
    #             ]
    #         }
    #     },
    #     "auth": auth,
    #     "id": 1
    # }
    values = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": "extend",
            "hostids": hostids
        },
        "auth": auth,
        "id": 1
    }
    data = json.dumps(values)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
    response = urllib2.urlopen(req, data)
    host_get = response.read()

    output = json.loads(host_get)

    try:
        message = output['result']
    except:
        message = output['error']['data']

    print json.dumps(message)


def get_groupids(url, auth, search=None):
    """ search the groupids by name
    """
    if search is not None:
        values = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "search": {
                    "name": [
                        search,
                    ]
                }
            },
            "auth": auth,
            "id": 1
        }
    else:
        values = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
            },
            "auth": auth,
            "id": 1
        }

    data = json.dumps(values)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
    response = urllib2.urlopen(req, data)
    host_get = response.read()

    output = json.loads(host_get)
    # print output
    try:
        message = output['result']
    except:
        message = output['error']['data']
    groupids = []
    for g in message:
        groupids.append(g["groupid"])
    print groupids


def get_hostids_by_groupids(url, auth, groupids):
    """ search the hostids by groupids
    """
    pass


def get_hostids_by_name(url, auth, search=None):
    """ search the hostids by hostname node
    """
    if search is not None:
        values = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "search": {
                    "host": [
                        search
                    ]
                }
            },
            "auth": auth,
            "id": 1
        }
    else:
        values = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
            },
            "auth": auth,
            "id": 1
        }
    # values = {
    #     "jsonrpc": "2.0",
    #     "method": "host.get",
    #     "params": {
    #         "output": "extend",
    #         "filter": {
    #             "host": [
    #                 "fpt-compute01",
    #                 "fpt-compute02"
    #             ]
    #         }
    #     },
    #     "auth": auth,
    #     "id": 1
    # }

    data = json.dumps(values)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
    response = urllib2.urlopen(req, data)
    host_get = response.read()

    output = json.loads(host_get)

    try:
        message = output['result']
    except:
        message = output['error']['data']
    hostids = []
    if message is not None:
        for m in message:
            hostids.append(m["hostid"])
    return hostids
    # print summary_metrics(message)
    # print json.dumps(message, indent=4, sort_keys=True)


def host_get_items(url, auth, hostids):
    # values = {
    #     "jsonrpc": "2.0",
    #     "method": "host.get",
    #     "params": {
    #         "output": "extend",
    #         "filter": {
    #             "host": [
    #                 "fpt-compute01",
    #             ]
    #         }
    #     },
    #     "auth": auth,
    #     "id": 1
    # }
    values = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": hostids,
            "search": {
                "key_": "collectd-libvirt.disk-ops-"
            },
            "sortfield": "name"
        },
        "auth": auth,
        "id": 1
    }
    data = json.dumps(values)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
    response = urllib2.urlopen(req, data)
    host_get = response.read()

    output = json.loads(host_get)

    try:
        message = output['result']
    except:
        message = output['error']['data']
    print summary_metrics(message)
    # print json.dumps(message, indent=4, sort_keys=True)


def summary_metrics(metrics):
    total = 0
    for metric in metrics:
        print "metric: %s vaule: %s" % (metric["key_"], metric["lastvalue"])
        total = float(total) + float(metric["lastvalue"])
    return total


def main():
    url = 'http://172.25.32.5/zabbix/api_jsonrpc.php'
    username = "Admin"
    password = "zabbix"

    # parser = argparse.ArgumentParser(description='Create Zabbix screen from all of a host Items or Graphs.')
    # parser.add_argument('hostname', metavar='H', type=str,
    #                     help='Zabbix Host to create screen from')
    # parser.add_argument('screenname', metavar='N', type=str,
    #                     help='Screen name in Zabbix.  Put quotes around it if you want spaces in the name.')
    # parser.add_argument('-c', dest='columns', type=int, default=3,
    #                     help='number of columns in the screen (default: 3)')
    # parser.add_argument('-d', dest='dynamic', action='store_true',
    #                     help='enable for dynamic screen items (default: disabled)')
    # parser.add_argument('-t', dest='screentype', action='store_true',
    #                     help='set to 1 if you want to create only simple graphs of items, no previously defined graphs will be added to screen (default 0)')

    # args = parser.parse_args()
    # hostname = args.hostname
    # screen_name = args.screenname
    # columns = args.columns
    # dynamic = (1 if args.dynamic else 0)
    # screentype = (1 if args.screentype else 0)

    auth = authenticate(url, username, password)
    # host_get(url, auth, 10108)
    # host_get_items(url, auth, 10108)
    # hostids = get_hostids(url, auth)
    # host_get_items(url, auth, hostids)

    get_groupids(url, auth, search="FPT")
    # graphids = getGraph(hostname, url, auth, screentype, dynamic, columns)

    # print "Screen Name: " + screen_name
    # print "Total Number of Graphs: " + str(len(graphids))

    # screenCreate(url, auth, screen_name, graphids, columns)


if __name__ == '__main__':
    main()
