from config import Secrets

import mysql.connector as mysql

from mysql.connector import MySQLConnection, errors
from typing import Tuple, List, Any, Union, Optional, TypeVar

__all__ = [
    "Database",
    "DB",
    "RowSet",
    "MultiRowSet",
    "ResultSet"
]

_RowSet = Optional[Tuple[Any, ...]]
_MultiRowSet = List[Tuple[Any, ...]]

RowSet = TypeVar("RowSet", bound=_RowSet)
MultiRowSet = TypeVar("MultiRowSet", bound=_MultiRowSet)
ResultSet = TypeVar("ResultSet", bound=Union[_MultiRowSet, _RowSet])


class Database:
    def __init__(self):
        self.__conn: Optional[MySQLConnection] = None

    def connect(self):
        try:
            self.__conn = mysql.connect(
                host=Secrets.db_host, port=Secrets.db_port,
                database=Secrets.db_name, user=Secrets.db_user, passwd=Secrets.db_passwd,
            )
        except errors.Error:
            self.__conn = None
        return self

    @property
    def is_connected(self) -> bool:
        return self.__conn is not None

    @staticmethod
    def _fetch(cursor, mode) -> ResultSet:
        if mode == "one":
            return cursor.fetchone()
        if mode == "many":
            return cursor.fetchmany()
        if mode == "all":
            return cursor.fetchall()

        return None

    def execute(self, query: str, values: Tuple = (), *, fetch: str = None) -> ResultSet:
        cursor = self.__conn.cursor()

        cursor.execute(query, values)
        data = self._fetch(cursor, fetch)

        cursor.close()
        return data

    def run(self, query: str, values: Tuple = ()) -> None:
        cursor = self.__conn.cursor()

        cursor.execute(query, values)
        self.__conn.commit()

        cursor.close()


DB = Database()
