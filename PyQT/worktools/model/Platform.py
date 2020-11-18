# -*- coding: utf-8 -*-
class Platform(object):

    def __init__(self):
        self._name = ''

    @property
    def Name(self):
        return self._name

    @property
    def Id(self):
        return self._id

    @property
    def Appid(self):
        return self._appid

    @property
    def Version(self):
        return self._version

    @property
    def Url(self):
        return self._url

    @property
    def ServerPath(self):
        return self._serverPath

    def parseQuery(self, query):
        self._id = query.value('id')
        self._name = query.value('name')
        self._url = query.value('url')
        self._appid = query.value('appid')
        self._version = query.value('version')
        self._serverPath = query.value('server_path')

        return self

    def __str__(self):
        return '{Platform [ID:%s Name:%s]}' % (self._id, self._name)
