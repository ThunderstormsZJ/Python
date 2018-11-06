
# -*- coding: utf-8 -*-
import logging
import os


class Logger(object):
    def __init__(self, name):
        logger = logging.getLogger(name=name)
        logger.setLevel(logging.DEBUG)
        logName = os.path.join(os.getcwd(), 'res', 'log', 'log.log')
        fmt = logging.Formatter("[%(levelname)s] [%(asctime)s] [%(filename)s->%(funcName)s] [%(lineno)d] - %(message)s", "%Y-%m-%d %H:%M:%S")

        # 输出到文件
        fh = logging.FileHandler(logName, 'a', encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(fmt=fmt)
        logger.addHandler(ch)

        self.logger = logger
        fh.close()

    def get_log(self):
        return self.logger

