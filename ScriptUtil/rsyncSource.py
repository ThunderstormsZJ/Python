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
        "originFiles": ["paiyou", "src"],
        "dstFile": "gamehall",
        "installGames": ["gamehall"],
        "ingoreFiles": [".svn", "ccs", ".vscode"],
        "useStudio": True,
    }
}


class Platform(object):
    def __init__(self, path):
        self.__path = path
        rootPath = os.path.split(self.__path)[-1]
        config = None
        for key, item in PALTFORM_DICT.items():
            if rootPath == item['root']:
                config = item
                break
        self.config = config
        self.parseConfig()

    def isExist(self):
        return True if self.config else False

    def parseConfig(self):
        if not self.isExist():
            return

        if self.config["useStudio"]:
            self.dstPath = os.path.join(self.__path, "frameworks", "runtime-src", "proj.android-studio",
                                        self.config["dstFile"] if self.config["dstFile"] else "app", "src", "main",
                                        "assets")
        else:
            self.dstPath = os.path.join(self.__path, "frameworks", "runtime-src", "proj.android")

    # 同步文件
    def syncFile(self):
        if not self.config:
            return
        FileUtils.clean_folder(self.dstPath)
        installList = []
        for file in self.config["originFiles"]:
            originPath = os.path.join(self.__path, file)
            for file in os.listdir(originPath):
                if self.config["installGames"] and file in self.config["installGames"]:
                    installList.append(os.path.join(originPath, file))

        self.installGames(installList)

    # FileUtils.copy_file_with_ignore(os.path.join(self.__path,))

    def installGames(self, installList):
        print('====================================Install====================================')
        for gamePath in installList:
            name = os.path.split(gamePath)[-1]
            print(getCurString(u"install [%s]" % name))
            FileUtils.copy_file_with_ignore(gamePath, self.dstPath, self.config["ingoreFiles"], None, False)
        print('==================================Install End==================================')

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
        return "[用于cocos自动打包脚本]"

    def run(self, argv):
        super(CocosAutoPackPlugin, self).run(argv)
        cocosPath = os.environ['COCOS_CONSOLE_ROOT']
        platform = Platform(self.currPath)
        if not platform.isExist(): return
        platform.syncFile()

        sys.exit()

        if self.isCompile:
            print(getCurString(u"开始编译Lua文件"))
            compile_cmd = "\"%s\" luacompile -s \"%s\" -d \"%s\" -e -k HSGameHall666 -b HSGame@2017" % (
                os.path.join(cocosPath, 'cocos'), dstSrcRoot, dstSrcRoot)
            subprocess.call(compile_cmd, shell=True)
            FileUtils.remove_file_with_ext(dstSrcRoot, '.lua')

        # 编译apk
        if self.isGenApk:
            outApkDir = os.path.join(self.currPath, 'apk')
            apk_cmd = "\"%s\" compile -p android --android-studio \"%s\" --ndk-mode none -m release --proj-dir \"%s\" -o \"%s\"" \
                      % (os.path.join(cocosPath, 'cocos'), self.useStudio, currPlatform.androidRoot, outApkDir)
            subprocess.call(apk_cmd, shell=True)

    def check_custom_options(self, args):
        self.isCompile = args.compile
        self.isGenApk = args.apk
        self.useStudio = args.use_studio

    def parse_args(self, parser):
        super(CocosAutoPackPlugin, self).parse_args(parser)
        # 解析参数
        parser.add_argument('-c', '--compile', dest='compile', action='store_true', help='compile lua file')
        parser.add_argument('-apk', dest='apk', action='store_true', help='build apk')
        parser.add_argument('-android-studio', dest='use_studio', action='store_true',
                            help='use android studio project')
        parser.add_argument('-f', '--file', dest='file', metavar='filename', nargs=1, default='all',
                            help='copy filename(res/src/all)')
        parser.add_argument('-p', '--platform', dest='platform', metavar='platformName', default='',
                            help='support platform: %s' % '/'.join(self.get_platforms()))

    def get_platforms(self):
        return PALTFORM_DICT.keys()

# if __name__ == '__main__':
#     # sys.exit(0)
#
#     # 复制资源
#     if 'res' in args.file or 'all' in args.file:
#         print getCurString(u"开始复制资源文件")
#         cleanFloder(dstResRoot)
#         formatCopyDes(copyFileWithIgnore, currPlatform.defultResRoot, dstResRoot, currPlatform.resIgnoreFiles)
#         if not currPlatform.isDefault:
#             formatCopyDes(copyFileWithIgnore, currPlatform.platResRoot, dstResRoot, currPlatform.resIgnoreFiles)
#
#     if 'src' in args.file or 'all' in args.file:
#         print getCurString(u"开始复制Lua代码")
#         cleanFloder(dstSrcRoot)
#         formatCopyDes(copyFileWithIgnore, currPlatform.defultSrcRoot, dstSrcRoot, currPlatform.srcIgnoreFiles)
#         if not currPlatform.isDefault:
#             formatCopyDes(copyFileWithIgnore, currPlatform.platSrcRoot, dstSrcRoot)
#         currPlatform.installGames()
#         # copy config.json file
#         configFile = os.path.join(currPlatform.androidRoot, "assets", "config.json")
#         if not os.path.exists(configFile):
#             shutil.copy2(os.path.join(path, "config.json"), configFile)
