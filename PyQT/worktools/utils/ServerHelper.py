# -*- coding: utf-8 -*-
import os
import os.path
import paramiko
from .SSHUtils import SSHUtils
from .Logger import Logger

# 配置属性
config = {
    # 本地项目路径
    'local_path': '',
    # 服务器项目路径
    'ssh_path': '',
    # ssh地址、端口、用户名、密码
    'hostname': '192.168.1.158',
    'port': 22,
    'username': 'zhoujun',
    'password': '13117960232',
}

log = Logger(__name__).get_log()


class ServerHelper(object):
    def __init__(self):
        self._SSHUtils = SSHUtils(**config)
        # ssh传输
        transport = paramiko.Transport((config['hostname'], config['port']))
        transport.connect(username=config['username'], password=config['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)

        self._sftp = sftp

    # 存在检查大小是否一样，不一样则上传
    def upload_file_with_compare(self, local_path, ssh_path, callback=None):
        if not os.path.exists(local_path):
            log.info('[%s 不存在]' % local_path)
            return
        # 检查文件是否存在，不存在直接上传
        if not self._SSHUtils.is_exist_file(ssh_path):
            self._sftp.put(local_path, ssh_path, callback=callback)
            log.info('[%s 上传成功]' % ssh_path)
        else:
            if not self._SSHUtils.compare_file_by_size(local_path, ssh_path):
                self._sftp.put(local_path, ssh_path, callback=callback)
                log.info('[%s 更新成功]' % ssh_path)

    # 从服务器获取文件
    def get_file(self, local_path, ssh_path, callback=None):
        if self._SSHUtils.is_exist_file(ssh_path):
            self._sftp.get(ssh_path, local_path, callback=callback)

    def close(self):
        self._SSHUtils.close()
        self._sftp.close()
