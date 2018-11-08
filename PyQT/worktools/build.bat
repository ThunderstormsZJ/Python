REM -F 打包单个exe -w 取消控制台
REM -v FILE, --version=FILE 加入版本信息文件
REM --upx-dir用于压缩文件
pyinstaller -F -w --version-file .\file_version_info.txt DeployCard.py --hidden-import logic --hidden-import model --hidden-import utils --hidden-import widgets