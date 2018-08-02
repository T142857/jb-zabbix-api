import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import zabbix_cloud

ids = ['28399', '1000000']


def test_get_history_by_itemid():
    assert zabbix_cloud.get_history_by_itemid(ids[0])


def test_get_history_by_not_exits_itemid():
    assert zabbix_cloud.get_history_by_itemid(ids[1]) == []


def test_get_history_by_without_itemid():
    l = not bool(len(zabbix_cloud.get_history_by_itemid()))
    assert l


def test_get_metrics_by_uuid():
    assert True


def test_datetime_to_epoch():
    assert True
