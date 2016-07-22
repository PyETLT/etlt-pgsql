import datetime
import unittest
from os import path

import pytz

from etlt_pgsql.writer.PgSqlLoaderWriter import PgSqlLoaderWriter


class PgSqlLoaderWriterTest(unittest.TestCase):
    """
    Test cases for PgSqlLoaderWriter.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test_types(self):
        filename_actual = path.abspath(path.dirname(__file__)) + '/PgSqlLoaderWriterTest/test_types.csv'
        filename_expected = path.abspath(path.dirname(__file__)) + '/PgSqlLoaderWriterTest/test_types.expected.csv'

        writer = PgSqlLoaderWriter(filename_actual)
        writer.fields = ['int', 'str', 'none', 'empty', 'date', 'datetime']
        rows = [{'int':   123,
                 'str':   'Ministry of Silly Walks',
                 'none':  None,
                 'empty': '',
                 'date':  datetime.date(1994, 1, 1),
                 'datetime':  datetime.datetime(1994, 1, 1, 23, 15, 30)},
                {'int':   123,
                 'str':   'мỉאַîśŧґỷ өƒ Šỉŀłỷ שׂǻĺκŝ',  # https://www.tienhuis.nl/utf8-generator
                 'none':  None,
                 'empty': '',
                 'date':  None,
                 'datetime':  datetime.datetime(2016, 1, 1, 23, 15, 30, tzinfo=pytz.timezone('UTC'))}]

        with writer:
            for row in rows:
                writer.writerow(row)

        with open(filename_actual, 'rt', encoding='utf8') as file:
            actual = file.read()

        with open(filename_expected, 'rt', encoding='utf8') as file:
            expected = file.read()

        self.assertEqual(actual, expected)

    # ------------------------------------------------------------------------------------------------------------------
    #  @todo test strings with tabs and EOL
    #  @todo test with lading and selecting data from actual PostgreSQL database

# ------------------------------------------------------------------------------------------------------------------
