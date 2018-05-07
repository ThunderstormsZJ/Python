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
        "installGames": ["paiyou/gamehall", "src"],
        "ingoreFiles": [".svn", "ccs", ".vscode"],
        "useStudio": True,
    }
}


class Platform(object):
    def __init__(self, path):
        self.__path = path
        root_path = os.path.split(self.__path)[-1]
        config = None
        for key, item in PALTFORM_DICT.items():
            if root_path == item['root']:
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
            self.dst_path = os.path.join(self.__path, "frameworks", "runtime-src", "proj.android-studio",
                                        self.config["dstFile"] if self.config["dstFile"] else "app", "src", "main",
                                        "assets")
        else:
            self.dst_path = os.path.join(self.__path, "frameworks", "runtime-src", "proj.android")

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
        if self.isGenApk:
            outApkDir = os.path.join(self.currPath, 'apk')
            apk_cmd = "\"%s\" compile -p android --android-studio \"%s\" --ndk-mode none -m release --proj-dir \"%s\" -o \"%s\"" \
                      % (os.path.join(cocos_path, 'cocos'), self.useStudio, currPlatform.androidRoot, outApkDir)
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
