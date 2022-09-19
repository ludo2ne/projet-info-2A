import time
import unittest

from business_object.table import Table
from dao.table_dao import TableDao


class TestAttackDao(unittest.TestCase):
    def test_create_table_ok(self):
        # GIVEN
        table_dao = TableDao()
        table = Table(numero=12)

        # WHEN
        created = table_dao.creer(table)

        # THEN
        self.assertTrue(created)
        self.assertIsNotNone(table.id)


if __name__ == '__main__':
    unittest.main()
