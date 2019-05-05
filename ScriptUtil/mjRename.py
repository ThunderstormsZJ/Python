#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import thunder
from shutil import copyfile
from TUtils import getCurString, FileUtils

folders = ["其他", "条", "筒", "万"]
num_map = {"一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
face_map = {"万": "0", "筒": "1", "条": "2"}
other_face_map = {
    "东风": "0x31",
    "南风": "0x32",
    "西风": "0x33",
    "北方": "0x34",
    "红中": "0x41",
    "發财": "0x42",
    "白板": "0x43",
    "春": "0x51",
    "夏": "0x52",
    "秋": "0x53",
    "冬": "0x54",
    "梅": "0x55",
    "兰": "0x56",
    "菊": "0x57",
    "竹": "0x58",
}
dire_map = {
    "1": "top-1-",
    "1+": "top-3-",
    "2": "left-1-",
    "2+": "left-3-",
    "3": "bottom-1-",
    "3+": "bottom-3-",
    "4": "right-1-",
    "4+": "right-3-",
}


# 麻将子重命名脚本
class MJRenamePlugin(thunder.Plugin):

    @staticmethod
    def plugin_name():
        return "mj_rename"

    @staticmethod
    def brief_description():
        return getCurString(u"[用于重命名麻将子]")

    def run(self, argv):
        super(MJRenamePlugin, self).run(argv)

        if not os.path.exists(self.filePath):
            print(getCurString(u"文件不存在"))
            return

        # 需要保存的文件夹
        save_path = os.path.join(self.filePath, "pattern")
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        else:
            FileUtils.clean_folder(save_path)
            os.mkdir(save_path)

        for folder in folders:
            root_path = os.path.join(self.filePath, folder)
            for f in os.listdir(root_path):
                if f in other_face_map:
                    v = int(other_face_map[f], 16)
                    faceV = v >> 4
                    realV = v & 0x0F
                else:
                    faceV = int(face_map[f[1]])
                    realV = int(num_map[f[0]])
                for flag, changeFlag in dire_map.items():
                    pngPath = os.path.join(root_path, f, f + flag + ".png")
                    pngPath1 = os.path.join(root_path, f, flag + ".png")
                    pngPath2 = os.path.join(root_path, f, f[0] + flag + ".png")
                    resPath = None
                    if os.path.exists(pngPath):
                        resPath = pngPath
                    elif os.path.exists(pngPath1):
                        resPath = pngPath1
                    elif os.path.exists(pngPath2):
                        resPath = pngPath2
                    elif len(f) > 1:
                        pngPath3 = os.path.join(root_path, f, f[1] + flag + ".png")
                        if os.path.exists(pngPath3):
                            resPath = pngPath3

                    if resPath:
                        copyfile(resPath, os.path.join(save_path, changeFlag + str(faceV) + str(realV) + ".png"))
                print(getCurString("[%s 转换完成]" % f))

    def check_custom_options(self, args):
        self.filePath = args.file

    def parse_args(self, parser):
        super(MJRenamePlugin, self).parse_args(parser)
        parser.add_argument(dest='file', help='mj path')
