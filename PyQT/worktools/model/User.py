# -*- coding: utf-8 -*-
import json


class User(object):
    def __init__(self):
        self._id = 0
        self._name = ""
        self._admin = False
        self._password = ""

    def parseQuery(self, query):
        self._id = query.value('id')
        self._name = query.value('name')
        self._admin = query.value('admin')
        self._password = query.value("password")

        return self

    @property
    def Id(self):
        return self._id

    @property
    def Name(self):
        return self._name

    @property
    def IsAdmin(self):
        return self._admin == 1

    @property
    def Password(self):
        return self._password

    def serialize(self):
        return json.dumps(self.__dict__)

    def invertSerialize(self, data):
        dataDict = json.loads(data)
        for key, value in self.__dict__.items():
            self.__dict__[key] = dataDict[key]

        return self

    def __str__(self):
        return "{User [name=%s]}" % self._name
