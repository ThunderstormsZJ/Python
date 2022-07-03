#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import thunder
from xml.dom.minidom import parse
from datetime import date
import xml.dom.minidom
import py7zr
import aioshutil
import subprocess
import threadpool
import asyncio

from Attribute import PluginDesAttribute
from TUtils import getCurString


class BackUpItem:
    def __init__(self):
        self.OriginPath = ""  # 原操作的文件/文件夹路径
        self.DestinationPath = ""  # 需要移动到的目的地
        self.IsCompression = False  # 是否需要压缩
        self.CMD = ""  # CMD指令

    def __format_xml_str2list(self, tStr):
        fList = []
        filterStr = tStr.replace('\n', '').strip()
        if filterStr.find(';') > 0:
            fList = list(map(lambda x: x.strip(), filterStr.split(';')))
            fList.pop()
        elif filterStr != '':
            fList.append(filterStr)

        return fList

    def get_origin_path_list(self):
        return self.__format_xml_str2list(self.OriginPath)

    def get_cmd_list(self):
        return self.__format_xml_str2list(self.CMD)

    def parse_xml_item(self, element):
        propertyNames = dir(self)
        for propertyName in propertyNames:
            propertyEle = element.getElementsByTagName(propertyName)
            if propertyEle and len(propertyEle) > 0 and len(propertyEle[-1].childNodes) > 0:
                propertyValue = propertyEle[-1].childNodes[0].data
                if propertyValue.lower() == "false" or propertyValue.lower() == "true":
                    propertyValue = bool(propertyValue)
                setattr(self, propertyName, propertyValue)
        return self


@PluginDesAttribute(name="nasbackup", description=getCurString(u"[Nas备份脚本]"))
class NasBackUpPlugin(thunder.Plugin):
    def run(self, argv):
        super(NasBackUpPlugin, self).run(argv)
        try:
            self.parse_xml()
        except Exception as e:
            self.logger.exception(e)

    # 解析xml （多线程）
    def parse_xml(self):
        self.logger.info(getCurString(u"备份开始"))
        xmlPath = os.path.join(self.scriptPath, "Res/NasBackFileConfig.xml")
        DOMTree = xml.dom.minidom.parse(xmlPath)
        collection = DOMTree.documentElement
        xmlItem = collection.getElementsByTagName("Item")
        args = list(map(lambda x: BackUpItem().parse_xml_item(x), xmlItem))

        backupPool = threadpool.ThreadPool(50)
        backupTasks = threadpool.makeRequests(self.run_backup, args)

        for backupTask in backupTasks:
            backupPool.putRequest(backupTask)

        backupPool.wait()

        self.logger.info(getCurString(u"备份结束"))

    # 执行备份
    def run_backup(self, backupItem: BackUpItem):
        # 执行命令
        cmdList = backupItem.get_cmd_list()
        for cmd in cmdList:
            subprocess.call(cmd, shell=True)
            self.logger.info(getCurString(u"CMD({0}) 执行成功".format(cmd)))

        originPathList = backupItem.get_origin_path_list()
        tasks = [self.run_move_file(originPath, backupItem.DestinationPath, backupItem.IsCompression) for originPath in originPathList]
        asyncio.set_event_loop(asyncio.new_event_loop())
        taskloop = asyncio.get_event_loop()
        taskloop.run_until_complete(asyncio.wait(tasks))

    async def run_move_file(self, originPath, desPath, isCompression):
        originSplit = os.path.split(originPath)
        # 压缩
        zipFileName = "{0}_{1}.7z".format(originSplit[1], date.today())
        zipFilePath = os.path.join(originSplit[0], zipFileName)
        isFolder = os.path.isdir(originPath)
        if isFolder and isCompression:
            with py7zr.SevenZipFile(zipFilePath, mode="w") as z:
                z.writeall(originPath, arcname=originSplit[1])
            self.logger.info(getCurString(u"{0} 压缩成功".format(zipFilePath)))
        # 移动到目标文件夹并重命名
        if os.path.exists(zipFilePath):
            # 重命名
            await aioshutil.move(zipFilePath, desPath)
            self.logger.info(getCurString(u"{0} 移动到 {1}".format(zipFilePath, desPath)))
        else:
            await aioshutil.move(originPath, desPath)
            self.logger.info(getCurString(u"{0} 移动到 {1}".format(originPath, desPath)))

    def check_custom_options(self, args):
        pass

    def parse_args(self, parser):
        super(NasBackUpPlugin, self).parse_args(parser)
