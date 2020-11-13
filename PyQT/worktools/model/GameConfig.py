# -*- coding: utf-8 -*-
class GameConfig(object):
    def __init__(self):
        self._id = 0
        self._user = None
        self._game = None
        self._config = None
        self._platform = None
        self._name = ""

    def __str__(self):
        return "{GameConfig [name=%s]}" % self._name
