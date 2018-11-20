# -*- coding: utf-8 -*-
import sys
import os


def get_source_path(path):
    if getattr(sys, 'frozen', False):  # 运行于 |PyInstaller| 二进制环境
        basedir = sys._MEIPASS
    else:  # 运行于一般Python 环境
        basedir = os.path.dirname(os.path.dirname(__file__))

    return os.path.join(basedir, path)


GameConfigFileJson = get_source_path('res/config/game.json')
UploadFileLocalJson = get_source_path(os.path.join('res', 'data', 'peipai.json'))
UploadFileSSHJson = '/data/gamehall_nationwide/Games/peipai/peipai.json'
CardResDir = get_source_path(os.path.join('res', 'card', 'MJ'))
