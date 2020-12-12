from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # commandsからコネクション情報をgetするのだが、そこでの返り値をオーバーライドしている！
            gi.return_value = True
            call_command('wait_for_db')  # wait_for_dbは自作のmanagementコマンド名
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            # なんて便利な書き方！get_itemの返り値をリストで渡して、初め5回はエラーを返すようにしている！
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
