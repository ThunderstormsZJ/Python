#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import sys


# 编码
# python3 中不需要考虑编码情况
# python3 将字符编码为二进制
def getCurString(s):
    if sys.version_info > (3, 0):
        return s
    import six
    import locale
    sys_lang, encoding = locale.getdefaultlocale()
    ret = ""
    if isinstance(s, six.string_types):
        ret = s.encode(encoding)
        # print(encoding)
    return ret


class FileUtils(object):
    #
    # ignore_files[list]:需要忽略的文件
    # ignore_folders[list]:需要忽略的文件夹
    #
    @staticmethod
    def copy_file_with_ignore(src, dst, ignore_folders=[], ignore_files=[], is_print=True):
        if not os.path.exists(src):
            print(getCurString(u"源文件[%s]不存在!") % str(src))
            return
        if not os.path.exists(dst):
            os.makedirs(dst)

        def __check_ignore_file(file, ignore_files):
            if not ignore_files:
                return False
            for ignore_file in ignore_files:
                if file.find(ignore_file) >= 0:
                    return True
            return False

        file_copy_count = 0
        for (root, dirs, files) in os.walk(src):
            dst_root = root.replace(src, dst)
            # check if ignore folder
            for ignore_folder in ignore_folders:
                if ignore_folder in dirs:
                    dirs.remove(ignore_folder)

            for d in dirs:
                dst_dir = os.path.join(dst_root, d)
                if not os.path.exists(dst_dir):
                    os.mkdir(dst_dir)

            for f in files:
                if __check_ignore_file(f, ignore_files):
                    continue
                res_file = os.path.join(root, f)
                dst_file = os.path.join(dst_root, f)
                file_copy_count = file_copy_count + 1
                shutil.copy2(res_file, dst_file)
                if is_print:
                    print(dst_file)

        return file_copy_count

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
    def clean_folder(path, is_print=True):
        if is_print:
            print(getCurString(u"清理目标文件夹:%s") % path)
        if not os.path.exists(path):
            return
        if not os.listdir(path):
            os.rmdir(path)
        else:
            import errno
            import stat

            # 没有权限
            def handle_remove_readonly(func, path, exc):
                excvalue = exc[1]
                if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
                    os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
                    func(path)
                else:
                    raise Exception

            shutil.rmtree(path, ignore_errors=False, onerror=handle_remove_readonly)

    @staticmethod
    def convert_path_to_cmd(path):
        ret = path
        if sys.platform == 'darwin':
            ret = path.replace("\ ", " ").replace(" ", "\ ")

        if sys.platform == 'win32':
            ret = "\"%s\"" % (path.replace("\"", ""))
        return ret

    @staticmethod
    def erase_ext(filePath: str):
        if os.path.isfile(filePath):
            filePath = os.path.basename(filePath)
        name, ext = os.path.splitext(filePath)
        return name, ext


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
