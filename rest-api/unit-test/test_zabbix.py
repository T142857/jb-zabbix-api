import unittest
from unittest.mock import patch
from zabbix_cloud import get_history_by_itemid


def mock_metrics():
    return []


class BasicTest(unittest.TestCase):
    # test with decorators
    @patch('zabbix_cloud.zx.call')  # Mock 'zx' module 'call' method.
    def test_get_history_by_itemid(self, fake_get_history):
        """Mocking using a decorator"""
        fake_get_history.return_value = mock_metrics()  # set fake  zabbix_cloud.zx.call(...) allways equal = []
        metrics = get_history_by_itemid(123, 'process_load')
        self.assertEqual(metrics, [])

    def test_get_history_by_itemid_with_context_mananger(self):
        """Mocking using a context manager"""
        with patch('zabbix_cloud.zx.call') as fake_get_history:
            fake_get_history.return_value = mock_metrics()   # set fake  zabbix_cloud.zx.call(...) allways equal = []
            metrics = get_history_by_itemid(123, 'process_load')
            self.assertEqual(metrics, [])


if __name__ == "__main__":
    unittest.main()
