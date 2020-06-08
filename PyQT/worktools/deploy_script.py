# -*- coding: utf-8 -*-
# 程序发布脚本
import os
import re
from logic import __version__

STORAGE_PATH = 'F:\\workspace\\DeployCard'
BUILD_FILE_PATH = 'F:\\workspace\\Python\\PyQT\\worktools\\DeployCard.spec'


def Run():
    # 更改file version的版本号
    curVersion = __version__
    versionFile = os.path.join(os.getcwd(), 'file_version_info.txt')
    versionText = ''
    with open(versionFile, 'r', encoding='utf-8') as f:
        versionText = f.read()

    match = re.sub(r"u'ProductVersion', u'.*'", ("u'ProductVersion', u'%s'" % curVersion), versionText)
    with open(versionFile, 'w', encoding='utf-8') as f:
        f.write(match)

    # 切换到仓库文件夹 继续项目打包
    os.chdir(STORAGE_PATH)
    os.popen('workon dc')

    buildCmd = 'pyupdater build --app-version=%s %s' % (curVersion, BUILD_FILE_PATH)
    result = os.popen(buildCmd)
    print(result.read())

    signCmd = 'pyupdater pkg --process --sign'
    result = os.popen(signCmd)
    print(result.read())

    updateCmd = 'pyupdater upload --service s3'
    result = os.popen(updateCmd)
    print(result.read())


if __name__ == '__main__':
    Run()
