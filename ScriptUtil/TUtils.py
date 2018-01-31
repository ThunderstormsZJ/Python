#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import locale

# 编码
def getCurString(s):
	sys_lang, encoding = locale.getdefaultlocale()
	ret = ""
	if isinstance(s, unicode):
		ret = s.encode(encoding)
	return ret

class FileUtils(object):
	#
	# ignoreFiles[list]:需要忽略的文件(文件夹)
	#
	@staticmethod
	def copyFileWithIgnore(src, dst, ignoreFiles=None, isPrint=True):
		# global COUNT
		if not os.path.exists(src):
			print getCurString(u"源文件[%s]不存在!") % str(src)
			return
		if not os.path.exists(dst):
			os.mkdir(dst)

		def __checkIgnoreFile(file, ignoreFiles):
			if not ignoreFiles:
				return False
			for ignoreFile in ignoreFiles:
				if os.path.isabs(ignoreFile) and file.rfind(ignoreFile)>=0:
					return True
				elif os.path.split(file)[1] == ignoreFile:
					return True
			return False

		fileList = os.listdir(src)
		for file in fileList:
			srcFile = os.path.join(src, file)
			dstFile = os.path.join(dst, file)

			if __checkIgnoreFile(srcFile, ignoreFiles):
				continue
			try:
				if os.path.isdir(srcFile):
					copyFileWithIgnore(srcFile, dstFile, ignoreFiles, isPrint)
				else:
					shutil.copy2(srcFile, dstFile)
					if isPrint:
						print srcFile
			except Exception as e:
				print e
				raise e
