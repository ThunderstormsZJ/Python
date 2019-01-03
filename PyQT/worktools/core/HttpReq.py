# -*- coding: utf-8 -*-
import json
from .Logger import Logger
from PyQt5.QtCore import QObject, QUrl, QByteArray, QUrlQuery
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

log = Logger(__name__).get_log()


class HttpReq(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.onSuccess = None
        self.onFailed = None
        self.m_netAccessManager = QNetworkAccessManager(self)
        self.m_netReply = None

    def request(self, httpUrl, sendData, on_success, on_fail, method):
        if self.m_netReply is not None:
            self.m_netReply.disconnect()
        if sendData is None:
            sendData = {}

        self.onSuccess = on_success
        self.onFailed = on_fail

        reqUrl = QUrl(httpUrl)
        req = QNetworkRequest(reqUrl)
        if method == 'get':
            reqQuery = QUrlQuery()
            for key, value in sendData.items():
                reqQuery.addQueryItem(str(key), str(value))
            reqUrl.setQuery(reqQuery)
            req.setUrl(reqUrl)
            print(reqUrl)
            self.m_netReply = self.m_netAccessManager.get(req)
        elif method == 'post':
            req.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
            senda = QByteArray()
            senda.append(self.convertDict(sendData))
            self.m_netReply = self.m_netAccessManager.post(req, senda)

        self.m_netReply.finished.connect(self.readData)
        self.m_netReply.error.connect(self.requesterr)

    def get(self, httpUrl, sendData, on_success, on_fail):
        self.request(httpUrl, sendData, on_success, on_fail, 'get')

    def post(self, httpUrl, sendData, on_success, on_fail):
        self.request(httpUrl, sendData, on_success, on_fail, 'post')

    def readData(self):
        recvData = self.m_netReply.readAll()
        data = str(bytes(recvData.data()), encoding='utf-8')

        try:
            print('data---->', data)
            result = json.loads(data, encoding='utf-8')
            self.onSuccess(result)
        except Exception as err:
            self.onFailed(err)

    def requesterr(self, err):
        log.error(err)

    def convertDict(self, dict):
        print('convert dict:', dict)
        str = ""
        index = 1
        for key, value in dict.items():
            if index == len(dict):
                str = str + '%s%s%s' % (key, '=', value)
            else:
                str = str + '%s%s%s%s' % (key, '=', value, '&')

            index += 1
        print('convert str:', str)
        return str
