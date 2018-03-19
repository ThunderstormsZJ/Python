#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
from xml.etree import ElementTree
from PIL import Image
import thunder
from TUtils import getCurString,FileUtils

class UnpackPlistPlugin(thunder.Plugin):

	@staticmethod
	def plugin_name():
		return "unpack_plist"

	@staticmethod
	def brief_description():
		return "UnpackPlist[用于解析Plist文件]"

	def run(self, argv):
		super(UnpackPlistPlugin,self).run(argv)

		if not os.path.exists(self.filePath):
			print(getCurString(u"文件不存在"))
			return
		if os.path.isdir(self.filePath):
			# 文件夹
			self.savePath = self.filePath + '_split'
			for f in os.listdir(self.filePath):
				if f.rfind("plist"):
					fileName = f.split(".")[0]
					self.savePath = os.path.join(self.filePath + '_split',fileName)
					plistFilePath = os.path.join(self.filePath,fileName + '.plist')
					pngFilePath = os.path.join(self.filePath,fileName + '.png')
					if not self.gen_png_from_plist(plistFilePath, pngFilePath):
						continue

		elif os.path.isfile(self.filePath):
			# plist 或者 png 文件
			fileRoot = os.path.split(self.filePath)[0]
			fileName = os.path.split(self.filePath)[1]
			fileName = fileName.split(".")[0]
			self.savePath = os.path.join(fileRoot,fileName)
			plistFilePath = os.path.join(fileRoot,fileName + '.plist')
			pngFilePath = os.path.join(fileRoot,fileName + '.png')
			self.gen_png_from_plist(plistFilePath, pngFilePath)

	def check_custom_options(self, args):
		self.filePath = args.file

	def parse_args(self, parser):
		super(UnpackPlistPlugin,self).parse_args(parser)
		parser.add_argument(dest='file', help='plist path')

	def tree_to_dict(self,tree):
		d = {}
		for index, item in enumerate(tree):
			if item.tag == 'key':
				if tree[index+1].tag == 'string':
					d[item.text] = tree[index + 1].text
				elif tree[index + 1].tag == 'true':
					d[item.text] = True
				elif tree[index + 1].tag == 'false':
					d[item.text] = False
				elif tree[index+1].tag == 'dict':
					d[item.text] = self.tree_to_dict(tree[index+1])
		return d
	
	def gen_png_from_plist(self, plist_filename, png_filename):
		if not os.path.exists(plist_filename):
			print(getCurString(u"plist[%s]文件不存在") % plist_filename)
			return False
		if not os.path.exists(png_filename):
			print(getCurString(u"png[%s]文件不存在") % png_filename)
			return False

		# 创建文件夹
		file_path = self.savePath
		FileUtils.clean_floder(file_path,False)
		os.mkdir(file_path)

		big_image = Image.open(png_filename)
		root = ElementTree.fromstring(open(plist_filename, 'r').read())
		plist_dict = self.tree_to_dict(root[0])
		to_list = lambda x: x.replace('{','').replace('}','').split(',')
		for k,v in plist_dict['frames'].items():
			if v.has_key('textureRect'):
				rectlist = to_list(v['textureRect'])
			elif v.has_key('frame'):
				rectlist = to_list(v['frame'])
			if v.has_key('rotated'):
				width = int( rectlist[3] if v['rotated'] else rectlist[2] )
				height = int( rectlist[2] if v['rotated'] else rectlist[3] )        
			else:
				width = int( rectlist[2] )
				height = int( rectlist[3] )
			box=( 
				int(rectlist[0]),
				int(rectlist[1]),
				int(rectlist[0]) + width,
				int(rectlist[1]) + height,
				)
			if v.has_key('spriteSize'):
				spriteSize = v['spriteSize']
			elif v.has_key('sourceSize'):
				spriteSize = v['sourceSize']
				
			sizelist = [ int(x) for x in to_list(spriteSize)]
			# print sizelist
			rect_on_big = big_image.crop(box)

			if (v.has_key('textureRotated') and v['textureRotated']) or (v.has_key('rotated') and v['rotated']):
				rect_on_big = rect_on_big.transpose(Image.ROTATE_90)
			
			sourceColorRectList = [0,0,int(rectlist[2]),int(rectlist[3])]
			if v.has_key('sourceColorRect'):
				sourceColorRectList = [ int(x) for x in to_list(v['sourceColorRect'])]

			result_image = Image.new(big_image.mode, sizelist, (0,0,0,0))
			result_box = (
				sourceColorRectList[0],
				sizelist[1] - sourceColorRectList[1] - sourceColorRectList[3],
				sourceColorRectList[0] + sourceColorRectList[2],
				sizelist[1] - sourceColorRectList[1],
			)
			result_image.paste(rect_on_big, result_box, mask=0)

			k = k.replace('/', '_')
			outfile = (file_path+'/' + k).replace('gift_', '')
			#print k
			if outfile.find('.png') == -1:
				outfile = outfile + '.png'
			# print outfile, "generated"
			result_image.save(outfile)
		print(getCurString(u"解析 plist[%s] png[%s] 成功") % (plist_filename, png_filename))
		return True
