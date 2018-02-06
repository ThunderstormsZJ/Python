#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
from TUtils import FileUtils,getCurString,ClassUtils

VERSION = "v1.0.0"
PluginsName = (
	"unpackPlist.UnpackPlistPlugin",
)
Plugins = {}

# 参考cocos脚本
class Plugin(object):
	def __init__(self):
		self.currPath = os.getcwd()

	@staticmethod
	def plugin_name():
		pass

	@staticmethod
	def brief_description():
		pass

	# Run it
	def run(self, argv):
		from argparse import ArgumentParser
		parser = ArgumentParser(prog="thunder %s" % self.__class__.plugin_name(),
			description=self.__class__.brief_description())
		self.parse_args(parser)
		(args, unkonw) = parser.parse_known_args(argv)
		self.check_custom_options(args)

	def check_custom_options(self, args):
		pass

	def parse_args(self, parser):
		pass

def parse_plugins():
	for classname in PluginsName:
		plugin_class = ClassUtils.get_class(classname)
		name = plugin_class.plugin_name()
		if name is None:
			print(getCurString("%s 插件没有名字") % classname)
			continue
		Plugins[name] = plugin_class

if __name__ == '__main__':
	if len(sys.argv) == 1 or sys.argv[1] in ('-h', '--help'):
		# help()
		sys.exit(0)

	if len(sys.argv) > 1 and sys.argv[1] in ('-v', '--version'):
		print("%s" % VERSION)
		sys.exit(0)

	parse_plugins()

	command = sys.argv[1]
	argv = sys.argv[2:]
	if Plugins[command]:
		plugin = Plugins[command]()
		plugin.run(argv)
	else:
		print(getCurString("命令错误"))
	