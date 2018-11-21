# -*- coding: utf-8 -*-
from PyQt5 import QtSql
from utils import singleton, Logger
from model import Platform

SqlConfig = {
    'host': '192.168.1.158',
    'database_name': 'dealcard_tool',
    'username': 'root',
    'password': '13117960232',
    'port': 37899
}
log = Logger(__name__).get_log()


@singleton
class SqlManager(object):

    def __init__(self):
        self._connectDB()

    def _connectDB(self):
        db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        db.setHostName(SqlConfig['host'])
        db.setDatabaseName(SqlConfig['database_name'])
        db.setUserName(SqlConfig['username'])
        db.setPassword(SqlConfig['password'])
        db.setPort(SqlConfig['port'])
        self._db = db
        if not db.open():
            log.error(db.lastError().driverText())
            raise Exception(db.lastError().driverText())
        else:
            return db

    def _checkConnect(self):
        # 重新连接
        if self._db.isOpen():
            self._db.open()

    def getPlatformInfo(self):
        platformList = []
        query = QtSql.QSqlQuery("SELECT * FROM platform")
        while query.next():
            platform = Platform().parseQuery(query)
            platformList.append(platform)
        return platformList

    def dispose(self):
        if self._db.isOpen():
            self._db.close()
