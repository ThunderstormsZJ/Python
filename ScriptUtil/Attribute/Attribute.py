#!/usr/bin/python
# -*- coding: utf-8 -*-
import inspect


class Attribute:
    AttributesMemberName = "__attributes__"
    _debug = False

    def __call__(self, func):
        # inherit attributes and append myself or create a new attributes list
        if (func.__dict__.__contains__(Attribute.AttributesMemberName)):
            func.__dict__[Attribute.AttributesMemberName].append(self)
        else:
            if inspect.isclass(func):
                setattr(func, Attribute.AttributesMemberName, [self])
            else:
                func.__setattr__(Attribute.AttributesMemberName, [self])
        return func

    def __str__(self):
        return self.__name__

    @classmethod
    def HasAttribute(cls, obj):
        if obj.__dict__.__contains__(Attribute.AttributesMemberName):
            attributeList = obj.__dict__[Attribute.AttributesMemberName]
            for attribute in attributeList:
                if isinstance(attribute, cls):
                    return True
        return False

    # 获取当前得属性
    @classmethod
    def GetAttribute(cls, obj):
        if obj.__dict__.__contains__(Attribute.AttributesMemberName):
            attributeList = obj.__dict__[Attribute.AttributesMemberName]
            for attribute in attributeList:
                if isinstance(attribute, cls):
                    return attribute
        return None

    @classmethod
    def GetAttributes(cls, obj):
        if obj.__dict__.__contains__(Attribute.AttributesMemberName):
            attributes = obj.__dict__[Attribute.AttributesMemberName]
            if isinstance(attributes, list):
                return [attribute for attribute in attributes if isinstance(attribute, cls)]
        return list()
