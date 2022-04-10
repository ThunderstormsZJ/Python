#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import thunder
import music_tag
import chardet

from Attribute import PluginDesAttribute
from TUtils import getCurString, FileUtils

@PluginDesAttribute(name="musictag", description=getCurString(u"[修改音乐文件tag]"))
class MusicTAGPlugin(thunder.Plugin):
    def run(self, argv):
        super(MusicTAGPlugin, self).run(argv)

        if not os.path.exists(self.filePath):
            print(getCurString(u"文件不存在"))
            return

        if os.path.isfile(self.filePath):
            self.write_lyrics_tag(self.filePath)
        elif os.path.isdir(self.filePath):
            self.walk_on(self.filePath)

    def walk_on(self, path):
        for f in os.listdir(path):
            fPath = os.path.join(path, f)
            if os.path.isfile(fPath):
                self.write_lyrics_tag(fPath)
            elif os.path.isdir(fPath):
                self.walk_on(fPath)

    def write_lyrics_tag(self, musicPath):
        try:
            music = music_tag.load_file(musicPath)
            lyrics = music['lyrics']
            if not lyrics:
                musicName, ext = FileUtils.erase_ext(musicPath)
                dirName = os.path.dirname(musicPath)
                # 查找歌词
                lrcPath = os.path.join(dirName, musicName + ".lrc")
                if os.path.exists(lrcPath):
                    with open(lrcPath, "rb") as lrc:
                        data = lrc.read()
                        encode = chardet.detect(data)['encoding']
                        music['lyrics'] = data.decode(encode)
                    music.save()
                    print(getCurString(u"music [{0}] => write lrc success".format(musicPath)))
        except Exception as e:
            pass

    def check_custom_options(self, args):
        self.filePath = args.file

    def parse_args(self, parser):
        super(MusicTAGPlugin, self).parse_args(parser)
        parser.add_argument(dest='file', help='path')
