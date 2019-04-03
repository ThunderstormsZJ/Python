# -*- coding: utf-8 -*-
# 一些基类的扩展和重写
from enum import Enum as BaseEnum
from enum import EnumMeta as BaseEnumMeta
from enum import _EnumDict
import inspect


class EnumMeta(BaseEnumMeta):
    def __new__(mcs, name, bases, attrs):
        Labels = attrs.get('Labels')

        if Labels is not None and inspect.isclass(Labels):
            del attrs['Labels']
            if hasattr(attrs, '_member_names'):
                attrs._member_names.remove('Labels')

        obj = BaseEnumMeta.__new__(mcs, name, bases, attrs)
        for m in obj:
            try:
                m.label = getattr(Labels, m.name)
            except AttributeError:
                m.label = m.name.replace('_', ' ').title()

        return obj


# reference enumfields of django
class EnumLabel(EnumMeta('Enum', (BaseEnum,), _EnumDict())):

    @classmethod
    def choices(cls):
        return tuple((m.value, m.label) for m in cls)

    def __str__(self):
        return self.label
