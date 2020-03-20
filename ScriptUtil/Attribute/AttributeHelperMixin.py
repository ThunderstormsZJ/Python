#!/usr/bin/python
# -*- coding: utf-8 -*-

from .Attribute import Attribute


class AttributeHelperMixin:
    def GetMethods(self):
        return {funcname: func
                for funcname, func in self.__class__.__dict__.items()
                if hasattr(func, '__dict__')
                }.items()

    def HasAttribute(self, method):
        if method.__dict__.__contains__(Attribute.AttributesMemberName):
            attributeList = method.__dict__[Attribute.AttributesMemberName]
            return isinstance(attributeList, list) and (len(attributeList) != 0)
        else:
            return False

    def GetAttributes(self, method):
        if method.__dict__.__contains__(Attribute.AttributesMemberName):
            attributeList = method.__dict__[Attribute.AttributesMemberName]
            if isinstance(attributeList, list):
                return attributeList
        return list()
