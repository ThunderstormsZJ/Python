#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import thunder
from shutil import copyfile, move
from TUtils import getCurString, FileUtils


# 麻将子重命名脚本
class PNGRename(thunder.Plugin):

    @staticmethod
    def plugin_name():
        return "png_rename"

    @staticmethod
    def brief_description():
        return getCurString(u"[用于更改PNG后缀]")

    def run(self, argv):
        super(PNGRename, self).run(argv)

        if not os.path.exists(self.filePath):
            print(getCurString(u"文件不存在"))
            return

        # 需要保存的文件夹
        save_path = os.path.join(self.filePath, "PNG")
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        else:
            FileUtils.clean_folder(save_path)
            os.mkdir(save_path)

        for f in os.listdir(self.filePath):
            if os.path.isfile(f):
                bytePath = os.path.join(self.filePath, f)
                prefixStr = b""
                with open(bytePath, "rb") as byteFile:
                    prefixStr = byteFile.readline(100)
                # Find PNG
                if prefixStr.find(b'RIF') != -1:
                    # copy file
                    if f.find(".png") > 0:
                        move(bytePath, os.path.join(save_path, f))
                    else:
                        move(bytePath, os.path.join(save_path, f+".png"))

    def check_custom_options(self, args):
        self.filePath = args.file

    def parse_args(self, parser):
        super(PNGRename, self).parse_args(parser)
        parser.add_argument(dest='file', help='png path')
