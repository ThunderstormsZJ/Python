#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
from TUtils import FileUtils

# 参考cocos脚本
class Plugin(object):
	@staticmethod
	def plugin_name():
		pass

	# Run it
	def run(self, argv):
		pass

	def _add_custom_options(self, parser):
		pass


if __name__ == '__main__':
	FileUtils.copyFileWithIgnore("","")
	