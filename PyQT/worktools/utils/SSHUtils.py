# -*- coding: utf-8 -*-
import paramiko
import os
from .Logger import Logger
log = Logger(__name__).get_log()


class SSHUtils(object):
    def __init__(self, **config):
        # ssh控制台
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=config['hostname'], port=config['port'], username=config['username'], password=config['password'])

        self._ssh = ssh

    # 检查文件夹是否存在，不存在则创建
    def check_folder(self, path):
        if self.is_exist_file(path) == 0:
            self._ssh.exec_command('mkdir ' + path)
            log.info('[%s 创建成功]' % path)

    # 判断文件是否存在
    def is_exist_file(self, path):
        stdin, stdout, stderr = self._ssh.exec_command('find ' + path)
        result = stdout.read().decode('utf-8')
        if len(result) == 0:
            log.info('[文件 %s 不存在]' % path)
            return False
        else:
            log.info('[文件 %s 存在]' % path)
            return True

    # 比较本地和服务端文件
    def compare_file_by_size(self, local_path, ssh_path):
        # 存在则比较文件大小
        # 本地文件大小
        lf_size = os.path.getsize(local_path)
        # 目标文件大小
        stdin, stdout, stderr = self._ssh.exec_command('du -b ' + ssh_path)
        result = stdout.read().decode('utf-8')
        tf_size = int(result.split('\t')[0])
        log.info('[本地文件大小为：%s，远程文件大小为：%s]' % (lf_size, tf_size))
        if lf_size == tf_size:
            log.info('[%s 大小与本地文件相同]' % ssh_path)
            return True
        else:
            log.info('[%s 大小与本地不相同]' % ssh_path)
            return False

    def close(self):
        self._ssh.close()
