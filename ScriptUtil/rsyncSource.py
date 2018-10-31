#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import thunder
from TUtils import getCurString, FileUtils

PALTFORM_DICT = {
    "paiyou": {
        "root": "paiyouhall",
        "dstFile": "gamehall",
        "installGames": ["paiyou/gamehall", "src", "paiyou/scduangoukamj"],
        "ingoreFiles": [".svn", "ccs", ".vscode"],
        "useStudio": True,
    },
}


class Platform(object):
    def __init__(self, path):
        self.__path = path
        self.dst_path = ""
        self.android_path = ""

        root_path = os.path.split(self.__path)[-1]
        config = None
        for key, item in PALTFORM_DICT.items():
            if root_path == item['root']:
                config = item
                break
        self.config = config
        self.use_studio = self.config["useStudio"]
        self.parseConfig()

    def isExist(self):
        return True if self.config else False

    def parseConfig(self):
        if not self.isExist():
            return

        if self.config["useStudio"]:
            self.android_path = os.path.join(self.__path, "frameworks", "runtime-src", "proj.android-studio")
            self.dst_path = os.path.join(self.android_path, self.config["dstFile"] if self.config["dstFile"] else "app",
                                         "src", "main", "assets")
        else:
            self.android_path = os.path.join(self.__path, "frameworks", "runtime-src", "proj.android")
            self.dst_path = self.android_path

    # 同步文件
    def syncFile(self):
        if not self.config:
            return
        FileUtils.clean_folder(self.dst_path)
        for install in self.config["installGames"]:
            print("[%s] install complete" % install)
            origin_install_path = install.split("/")
            resource_path = os.path.join(self.__path, *origin_install_path)
            destination_path = os.path.join(self.dst_path, *origin_install_path)

            FileUtils.copy_file_with_ignore(resource_path, destination_path, self.config["ingoreFiles"], [], False)

    # 根据install.lua文件获取游戏安装目录
    # def getGameInstallList(self):
    #     import lupa
    #     gameList = []
    #     if self.isDefault:
    #         return gameList
    #     installFile = open(
    #         os.path.join(self.__path, self.platSrcRoot, 'install.lua'))
    #     content = ""
    #     try:
    #         content = installFile.read()
    #     except Exception as e:
    #         print(e)
    #         print('install file parse error')
    #         sys.exit(0)
    #     finally:
    #         installFile.close()
    #     luaRuntime = lupa.LuaRuntime()
    #     installList = luaRuntime.execute(content)
    #     for g in installList.values():
    #         gameList.append(g.pkgName.split(".")[1])
    #     gameList.append('gamecommon')
    #     return gameList


class CocosAutoPackPlugin(thunder.Plugin):
    @staticmethod
    def plugin_name():
        return "auto_pack"

    @staticmethod
    def brief_description():
        return getCurString(u"[用于cocos自动打包脚本]")

    def run(self, argv):
        super(CocosAutoPackPlugin, self).run(argv)
        cocos_path = os.environ['COCOS_CONSOLE_ROOT']
        platform = Platform(self.currPath)
        if not platform.isExist():
            return
        platform.syncFile()

        if self.isCompile:
            print(getCurString(u"开始编译Lua文件"))
            compile_cmd = "\"%s\" luacompile -s \"%s\" -d \"%s\" -e -k HSGameHall666 -b HSGame@2017" % (
                os.path.join(cocos_path, 'cocos'), platform.dst_path, platform.dst_path)
            subprocess.call(compile_cmd, shell=True)
            FileUtils.remove_file_with_ext(platform.dst_path, '.lua')

        # 编译apk
        # if self.isGenApk:
        #     outApkDir = os.path.join(self.currPath, 'apk')
        #     apk_cmd = "\"%s\" compile -p android --android-studio \"%s\" --ndk-mode none -m release --proj-dir \"%s\" -o \"%s\"" \
        #               % (os.path.join(cocos_path, 'cocos'), platform.use_studio, platform.android_path, outApkDir)
        #     subprocess.call(apk_cmd, shell=True)

    def check_custom_options(self, args):
        self.isCompile = args.compile
        self.isGenApk = args.apk

    def parse_args(self, parser):
        super(CocosAutoPackPlugin, self).parse_args(parser)
        # 解析参数
        parser.add_argument('-c', '--compile', dest='compile', action='store_true', help='compile lua file')
        parser.add_argument('-apk', dest='apk', action='store_true', help='build apk')
        parser.add_argument('-f', '--file', dest='file', metavar='filename', nargs=1, default='all',
                            help='copy filename(res/src/all)')
        parser.add_argument('-p', '--platform', dest='platform', metavar='platformName', default='',
                            help='support platform: %s' % '/'.join(self.get_platforms()))

    def get_platforms(self):
        return PALTFORM_DICT.keys()
