#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import sys


# 编码
# python3 中不需要考虑编码情况
# python3 将字符编码为二进制
def getCurString(s):
    # import six
    # import locale
    # sys_lang, encoding = locale.getdefaultlocale()
    # ret = ""
    # if isinstance(s, six.string_types):
    #     ret = s.encode(encoding)
    #     print(encoding)
    return s


class FileUtils(object):
    #
    # ignoreFiles[list]:需要忽略的文件
    # ignoreFloders[list]:需要忽略的文件夹
    #
    @staticmethod
    def copy_file_with_ignore(src, dst, ignoreFloders=None, ignoreFiles=None, isPrint=True):
        if not os.path.exists(src):
            print(getCurString(u"源文件[%s]不存在!") % str(src))
            return
        if not os.path.exists(dst):
            os.mkdir(dst)

        def __checkIgnoreFile(file, ignoreFiles):
            if not ignoreFiles:
                return False
            for ignoreFile in ignoreFiles:
                if file.find(ignoreFile) >= 0:
                    return True
            return False

        def __checkIgnoreFloder(floder, ignoreFloders):
            if not ignoreFloders:
                return False
            for ignoreFloder in ignoreFloders:
                if os.path.isabs(ignoreFloder) and floder.rfind(ignoreFloder) >= 0:
                    return True
                elif floder.rfind(ignoreFloder) >= 0:
                    return True
            return False

        fileCopyCount = 0
        for (root, dirs, files) in os.walk(src):
            dstRoot = root.replace(src, dst)
            isIgnore = False
            for d in dirs:
                dstDir = os.path.join(dstRoot, d)
                print(dstDir)
                if __checkIgnoreFloder(dstDir, ignoreFloders):
                    isIgnore = True
                    continue
                if not os.path.exists(dstDir):
                    os.mkdir(dstDir)

            if isIgnore:
                continue
            print("---------------------")
            print(dstRoot, isIgnore)

            for f in files:
                if __checkIgnoreFile(f, ignoreFiles):
                    continue
                resFile = os.path.join(root, f)
                dstFile = os.path.join(dstRoot, f)
                fileCopyCount = fileCopyCount + 1
                # shutil.copy2(resFile, dstFile)
                if isPrint:
                    print(dstFile)

        return fileCopyCount

    # 移除ext后缀的文件
    @staticmethod
    def remove_file_with_ext(work_dir, ext):
        file_list = os.listdir(work_dir)
        for f in file_list:
            full_path = os.path.join(work_dir, f)
            if os.path.isdir(full_path):
                FileUtils.remove_file_with_ext(full_path, ext)
            elif os.path.isfile(full_path):
                name, cur_ext = os.path.splitext(f)
                if cur_ext == ext:
                    os.remove(full_path)

    # 清理文件夹
    @staticmethod
    def clean_floder(path, isPrint=True):
        if isPrint:
            print(getCurString(u"清理目标文件夹:%s") % path)
        if not os.path.exists(path):
            return
        if not os.listdir(path):
            os.rmdir(path)
        else:
            import errno, stat
            # 没有权限
            def handleRemoveReadonly(func, path, exc):
                excvalue = exc[1]
                if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
                    os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
                    func(path)
                else:
                    raise Exception

            shutil.rmtree(path, ignore_errors=False, onerror=handleRemoveReadonly)

    @staticmethod
    def convert_path_to_cmd(path):
        ret = path
        if sys.platform == 'darwin':
            ret = path.replace("\ ", " ").replace(" ", "\ ")

        if sys.platform == 'win32':
            ret = "\"%s\"" % (path.replace("\"", ""))
        return ret


class ClassUtils(object):
    @staticmethod
    def get_class(kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        if len(parts) == 1:
            m = sys.modules[__name__]
            m = getattr(m, parts[0])
        else:
            m = __import__(module)
            for comp in parts[1:]:
                m = getattr(m, comp)
        return m
