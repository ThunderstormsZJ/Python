# -*- mode: python -*-

block_cipher = None

added_files = [
]
a = Analysis(['WorkTool.py'],
             pathex=['F:\\workspace\\Python\\PyQT\\worktools'],
             binaries=[],
             datas=added_files,
             hiddenimports=['logic', 'model', 'core', 'widgets'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
extra_tree = Tree('F:\\workspace\\Python\\PyQT\\worktools\\res', prefix = 'res')
exe = EXE(pyz,
          a.scripts,
          extra_tree,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='win',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , version='F:\\workspace\\Python\\PyQT\\worktools\\file_version_info.txt')
