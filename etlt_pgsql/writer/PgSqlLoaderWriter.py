"""
ETLT-pgSQL

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import datetime
import os

import pytz
from etlt.writer.SqlLoaderWriter import SqlLoaderWriter


class PgSqlLoaderWriter(SqlLoaderWriter):
    """
    Writer for storing rows in CSV format optimized for PostgreSQL and 'copy from stdin' statement.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_bool(value, file):
        """
        Writes a boolean as a field to a CSV file.

        :param bool value: The boolean.
        :param T file: The file.
        """
        if value:
            file.write('1')
        else:
            file.write('0')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_date(value, file):
        """
        Writes a date as a field to a CSV file.

        :param datetime.date value: The date.
        :param T file: The file.
        """
        file.write(value.isoformat())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_datetime(value, file):
        """
        Writes a datetime as a field to a CSV file.

        :param datetime.datetime value: The date.
        :param T file: The file.
        """
        zone = value.tzinfo
        if zone and zone != pytz.utc:
            raise ValueError('Only native and UTC timezone supported')
        file.write(value.isoformat())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_timedelta(value, file):
        """
        Writes a timedelta as a field to a CSV file.

        :param datetime.timedelta value: The timedelta.
        :param T file: The file.
        """
        PgSqlLoaderWriter.write_string(str(value), file)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_decimal(value, file):
        """
        Writes a decimal as a field to a CSV file.

        :param decimal.Decimal value: The decimal.
        :param T file: The file.
        """
        file.write(str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_float(value, file):
        """
        Writes a float as a field to a CSV file.

        :param float value: The float.
        :param T file: The file.
        """
        file.write(str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_int(value, file):
        """
        Writes an integer as a field to a CSV file.

        :param int value: The integer.
        :param T file: The file.
        """
        file.write(str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_none(_, file):
        """
        Writes None as a field to a CSV file.

        :param None _: The None object.
        :param T file: The file.
        """
        file.write('\\N')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_string(value, file):
        """
        Writes a string as a field to a CSV file.

        :param str value: The string.
        :param T file: The file.
        """
        if value == '':
            file.write('\\N')
        else:
            file.write("'")
            file.write(value.replace('\\', '\\\\').replace("'", "\\'"))
            file.write("'")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_uuid(value, file):
        """
        Writes a UUID as a field to a CSV file.

        :param uuid.UUID value: The UUID.
        :param T file: The file.
        """
        PgSqlLoaderWriter.write_string(str(value), file)

    # ------------------------------------------------------------------------------------------------------------------
    def writerow(self, row):
        """
        Writes a row to the destination file.

        :param dict[str,str|None] row: The row.
        """
        for i, field in enumerate(self._fields):
            if i:
                self._file.write(',')
            self._write_field(row[field])

        self._file.write(os.linesep)

    # ------------------------------------------------------------------------------------------------------------------
    def get_bulk_load_sql(self, table_name):
        """
        Returns a SQL statement for bulk loading the data into a table.

        :param str table_name: The name of the table.

        :rtype: str
        """
        sql = "copy {TABLE_NAME} from stdin csv"
        sql += " delimiter ','"
        sql += " null '\\N'"
        sql += " quote '\'\''"
        sql += " escape '\\'"
        sql += " encoding '{ENCODING}'"

        return sql.format(ENCODING=self._encoding, TABLE_NAME=table_name)


# ----------------------------------------------------------------------------------------------------------------------
PgSqlLoaderWriter.register_handler("<class 'bool'>", PgSqlLoaderWriter.write_bool)
PgSqlLoaderWriter.register_handler("<class 'datetime.date'>", PgSqlLoaderWriter.write_date)
PgSqlLoaderWriter.register_handler("<class 'datetime.datetime'>", PgSqlLoaderWriter.write_datetime)
PgSqlLoaderWriter.register_handler("<class 'datetime.timedelta'>", PgSqlLoaderWriter.write_timedelta)
PgSqlLoaderWriter.register_handler("<class 'decimal.Decimal'>", PgSqlLoaderWriter.write_decimal)
PgSqlLoaderWriter.register_handler("<class 'float'>", PgSqlLoaderWriter.write_float)
PgSqlLoaderWriter.register_handler("<class 'int'>", PgSqlLoaderWriter.write_int)
PgSqlLoaderWriter.register_handler("<class 'NoneType'>", PgSqlLoaderWriter.write_none)
PgSqlLoaderWriter.register_handler("<class 'str'>", PgSqlLoaderWriter.write_string)
PgSqlLoaderWriter.register_handler("<class 'uuid.UUID'>", PgSqlLoaderWriter.write_uuid)
