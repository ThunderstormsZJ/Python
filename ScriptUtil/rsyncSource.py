#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import sys
import subprocess
import thunder
from TUtils import getCurString,FileUtils

class Platform(object):
	def __init__(self, path):
		self.__path = path
		self.__platformList = []
		self.isDefault = False
		self.defultSrcRoot = os.path.join(self.__path, "src")
		self.defultResRoot = os.path.join(self.__path, "res")
		self.srcIgnoreFiles = [".svn", ".git", ".vscode", ".gitignore"]
		self.resIgnoreFiles = [".svn", "mp3"]

		self.defultAndroidRoot = os.path.join(path, "frameworks", "runtime-src", "proj.android")
		self._findPlatform()

	def _findPlatform(self):
		# 查询当前目录所有平台
		for file in os.listdir(self.__path):
			if file.find("res") == 0 and "_" in file:
				self.__platformList.append(file.split("_")[1])

	def getPlatformList(self):
		return self.__platformList

	# 根据install.lua文件获取游戏安装目录
	def getGameInstallList(self):
		import lupa
		gameList = []
		if self.isDefault:
			return gameList
		installFile = open(
			os.path.join(self.__path, self.platSrcRoot, 'install.lua'))
		content = ""
		try:
			content = installFile.read()
		except Exception as e:
			print(e)
			print('install file parse error')
			sys.exit(0)
		finally:
			installFile.close()
		luaRuntime = lupa.LuaRuntime()
		installList = luaRuntime.execute(content)
		for g in installList.values():
			gameList.append(g.pkgName.split(".")[1])
		gameList.append('gamecommon')
		return gameList

	def installGames(self):
		if self.isDefault:
			return
		installSrc = os.path.join(self.__path, self.defultSrcRoot, 'app', 'games')
		installDst = os.path.join(self.__path, self.androidRoot, 'assets', 'src', 'app', 'games')
		installResSrc = os.path.join(self.__path, self.defultResRoot, 'games')
		installResDst = os.path.join(self.__path, self.androidRoot, 'assets', 'res', 'games')
		resWhiteList = ['MJ','poker','zipai']

		FileUtils.clean_floder(installDst)
		FileUtils.clean_floder(installResDst)
		os.mkdir(installDst)
		os.mkdir(installResDst)
		
		print( '====================================Install====================================')
		for game in self.getGameInstallList():
			print('install game:[%s]' % str(game))
			copyFileWithIgnore(os.path.join(installSrc, game), os.path.join(installDst, game), ['.svn'], False)
			if self.__isCopyRes:
				copyFileWithIgnore(os.path.join(installResSrc, game), os.path.join(installResDst, game), ['.svn'], False)
		if self.__isCopyRes:
			for extend in resWhiteList:
				print('install extendRes:[%s]' % extend)
				copyFileWithIgnore(os.path.join(installResSrc, extend), os.path.join(installResDst, extend), ['.svn'], False)
		print( '==================================Install End==================================')

	def getCurrentPlatform(self, args):
		self.__isCopyRes = args.file == 'res' or args.file == 'all'
		name = args.platform
		if name:
			if name in self.__platformList:
				self.platSrcRoot = os.path.join(self.__path, "src_%s" % name)
				self.platResRoot = os.path.join(self.__path, "res_%s" % name)
				self.androidRoot = os.path.join(path, "frameworks", "runtime-src", "proj.android_%s" % name)
				if name == 'gdxn' or not os.path.exists(self.androidRoot):
					self.androidRoot = self.defultAndroidRoot
				installSrc = os.path.join(self.__path, self.defultSrcRoot, 'app', 'games')
				installResSrc = os.path.join(self.__path, self.defultResRoot, 'games')
				self.resIgnoreFiles.append(installResSrc)
				self.srcIgnoreFiles.append(installSrc)
				return self
			else:
				return None
		else:
			# 返回默认
			self.isDefault = True
			self.androidRoot = self.defultAndroidRoot
			return self

class CocosAutoPackPlugin(thunder.Plugin):
	@staticmethod
	def plugin_name():
		return "auto_pack"

	@staticmethod
	def brief_description():
		return "[用于cocos自动打包脚本]"

	def run(self, argv):
		super(UnpackPlistPlugin,self).run(argv)
		cocosPath = os.environ['COCOS_CONSOLE_ROOT']
		platform = Platform(self.currPath)
		# 获取当前平台
		currPlatform = platform.getCurrentPlatform(args)
		if not currPlatform:
			print(getCurString(u'%s 平台不存在') % args.platform)
			sys.exit(0)

		dstSrcRoot = os.path.join(currPlatform.androidRoot, "assets", "src")
		dstResRoot = os.path.join(currPlatform.androidRoot, "assets", "res")

	
	def check_custom_options(self, args):


	def parse_args(self, parser):
		super(UnpackPlistPlugin,self).parse_args(parser)
		# 解析参数
		parser.add_argument('-c', '--compile', dest='compile', action='store_true', help='compile lua file')
		parser.add_argument('-apk', dest='apk', action='store_true', help='build apk')
		parser.add_argument('-f', '--file', dest='file', metavar='filename', nargs=1, default='all', help='copy filename(res/src/all)')
		parser.add_argument('-p', '--platform', dest='platform', metavar='platformName', default='',
			help='support platform: %s' % '/'.join(platform.getPlatformList()))


if __name__ == '__main__':
	# sys.exit(0)

	# 复制资源
	if 'res' in args.file or 'all' in args.file:
		print getCurString(u"开始复制资源文件")
		cleanFloder(dstResRoot)
		formatCopyDes(copyFileWithIgnore, currPlatform.defultResRoot, dstResRoot, currPlatform.resIgnoreFiles)
		if not currPlatform.isDefault:
			formatCopyDes(copyFileWithIgnore, currPlatform.platResRoot, dstResRoot, currPlatform.resIgnoreFiles)

	if 'src' in args.file or 'all' in args.file:
		print getCurString(u"开始复制Lua代码")
		cleanFloder(dstSrcRoot)
		formatCopyDes(copyFileWithIgnore, currPlatform.defultSrcRoot, dstSrcRoot, currPlatform.srcIgnoreFiles)
		if not currPlatform.isDefault:
			formatCopyDes(copyFileWithIgnore, currPlatform.platSrcRoot, dstSrcRoot)
		currPlatform.installGames()
		# copy config.json file
		configFile = os.path.join(currPlatform.androidRoot, "assets", "config.json")
		if not os.path.exists(configFile):
			shutil.copy2(os.path.join(path, "config.json"), configFile)

	if args.compile:
		print getCurString(u"开始编译Lua文件")
		compile_cmd = "\"%s\" luacompile -s \"%s\" -d \"%s\" -e -k HSGameHall666 -b HSGame@2017" % (os.path.join(cocosPath,'cocos'), dstSrcRoot, dstSrcRoot)
		subprocess.call(compile_cmd, shell=True)

		remove_file_with_ext(dstSrcRoot,'.lua')

	# 编译apk
	if args.apk:
		outApkDir = os.path.join(path, 'apk')
		apk_cmd = "\"%s\" compile -p android --ndk-mode none -m release --proj-dir \"%s\" -o \"%s\"" % (os.path.join(cocosPath,'cocos'), currPlatform.androidRoot, outApkDir)
		subprocess.call(apk_cmd, shell=True)

