REM -F �������exe -w ȡ������̨
REM -v FILE, --version=FILE ����汾��Ϣ�ļ�
REM --upx-dir����ѹ���ļ�
pyinstaller -F -w --version-file .\file_version_info.txt DeployCard.py --hidden-import logic --hidden-import model --hidden-import utils --hidden-import widgets