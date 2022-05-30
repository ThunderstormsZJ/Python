#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import thunder
from xml.dom.minidom import parse
import xml.dom.minidom
import py7zr
import shutil

from Attribute import PluginDesAttribute
from TUtils import getCurString

class BackUpItem:
    def __init__(self):
        self.OriginPath = "" #原操作的文件/文件夹路径
        self.DestinationPath = "" #需要移动到的目的地
        self.IsCompression = False #是否需要压缩
        self.IsFolder = False #是否是文件夹

    def parse_xml_item(self, element):
        propertyNames = dir(self)
        for propertyName in propertyNames:
            propertyEle = element.getElementsByTagName(propertyName)
            if propertyEle:
                propertyValue = propertyEle[-1].childNodes[0].data
                if propertyValue.lower() == "false" or propertyValue.lower() == "true":
                    propertyValue = bool(propertyValue)
                setattr(self, propertyName, propertyValue)

        self.IsFolder = os.path.isdir(self.OriginPath)

@PluginDesAttribute(name="nasbackup", description=getCurString(u"[Nas备份脚本]"))
class NasBackUpPlugin(thunder.Plugin):
    def run(self, argv):
        super(NasBackUpPlugin, self).run(argv)
        self.parse_xml()

    # 解析xml
    def parse_xml(self):
        xmlPath =  os.path.join(self.scriptPath, "Res/NasBackFileConfig.xml")
        DOMTree = xml.dom.minidom.parse(xmlPath)
        collection = DOMTree.documentElement
        folders = collection.getElementsByTagName("Item")
        for folder in folders:
            item = BackUpItem()
            item.parse_xml_item(folder)
            self.run_backup(item)

    # 执行备份
    def run_backup(self, backupItem: BackUpItem):
        originSplit = os.path.split(backupItem.OriginPath)

        # 压缩
        zipFileName = originSplit[1]+".7z"
        zipFilePath = os.path.join(originSplit[0], zipFileName)
        if backupItem.IsFolder and backupItem.IsCompression:
            with py7zr.SevenZipFile(zipFilePath, mode="w") as z:
                z.writeall(backupItem.OriginPath, arcname=originSplit[1])
            print(getCurString(u"{0} 压缩成功".format(zipFileName)))

        # 移动到目标文件夹并重命名
        if os.path.exists(zipFilePath):
            # 重命名
            shutil.move(zipFilePath, backupItem.DestinationPath)
            print(getCurString(u"{0} 移动成功".format(zipFilePath)))
        else:
            shutil.move(backupItem.OriginPath, backupItem.DestinationPath)
            print(getCurString(u"{0} 移动到 {1}".format(backupItem.OriginPath, backupItem.DestinationPath)))


    def check_custom_options(self, args):
        pass

    def parse_args(self, parser):
        super(NasBackUpPlugin, self).parse_args(parser)
