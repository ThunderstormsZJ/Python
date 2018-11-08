# -*- mode: python -*-

block_cipher = None


a = Analysis(['¨Cversion-file', 'file_version_info.txt', 'DeployCard.py'],
             pathex=['F:\\workspace\\Python\\PyQT\\worktools'],
             binaries=[],
             datas=[],
             hiddenimports=['logic', 'model', 'utils', 'widgets'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='¨Cversion-file',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
