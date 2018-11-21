# -*- coding: utf-8 -*-
class Platform(object):

    def __init__(self):
        self._name = ''

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def appid(self):
        return self._appid

    @property
    def version(self):
        return self._version

    @property
    def url(self):
        return self._url

    def parseQuery(self, query):
        self._id = query.value('id')
        self._name = query.value('name')
        self._url = query.value('url')
        self._appid = query.value('appid')
        self._version = query.value('version')

        return self

    def __str__(self):
        return '{Platform [ID:%s Name:%s]}' % (self._id, self._name)
