#!/usr/bin/python
# -*- coding: utf-8 -*-

from .Attribute import Attribute


class PluginDesAttribute(Attribute):
    __name = None
    __description = None

    def __init__(self, name, description):
        super().__init__()
        self.__name = name
        self.__description = description

    @property
    def Name(self):
        return self.__name

    @property
    def Description(self):
        return self.__description
