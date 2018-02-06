#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import sys
import time
import subprocess
import locale
from argparse import ArgumentParser

# COUNT = 0

# def formatCopyDes(fun, *agrs):
# 	global COUNT
# 	startTime = int(time.time())
# 	fun(*agrs)
# 	endTime = int(time.time())

# 	print getCurString(u"复制完成,总计复制 %s 文件,使用时间 %s s") % (COUNT, str(endTime - startTime))
# 	COUNT = 0

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
		self.__findPlatform()

	def __findPlatform(self):
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
		cleanFloder(installDst)
		cleanFloder(installResDst)

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
		# self.__isCompile = args.compile
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
			# self.platSrcRoot = ""
			# self.platResRoot = ""
			self.androidRoot = self.defultAndroidRoot
			return self


if __name__ == '__main__':
	path = os.path.abspath(os.path.dirname(__file__))
	cocosPath = os.environ['COCOS_CONSOLE_ROOT']
	platform = Platform(path)
	# 解析参数
	parser = ArgumentParser(description="copy resourcs and build ndk")
	parser.add_argument('-c', '--compile', dest='compile', action='store_true', help='compile lua file')
	parser.add_argument('-apk', dest='apk', action='store_true', help='compile lua file')
	parser.add_argument('-f', '--file', dest='file', metavar='filename', nargs=1, default='all', help='copy filename(res/src/all)')
	parser.add_argument('-p', '--platform', dest='platform', metavar='platformName', default='',
		help='support platform: %s' % '/'.join(platform.getPlatformList()))
	args = parser.parse_args()

	# 获取当前平台
	currPlatform = platform.getCurrentPlatform(args)
	if not currPlatform:
		print(getCurString(u'%s 平台不存在') % args.platform)
		sys.exit(0)

	dstSrcRoot = os.path.join(currPlatform.androidRoot, "assets", "src")
	dstResRoot = os.path.join(currPlatform.androidRoot, "assets", "res")
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

