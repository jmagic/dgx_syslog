# -*- mode: python -*-
a = Analysis(['dgx_syslogger.py'],
             pathex=['C:\\Users\\jim.maciejewski\\Documents\\dgx_syslog'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)


pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='dgx_syslogger.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='dgx_syslog.ico' )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='dgx_syslogger')
