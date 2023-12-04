# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/sarah/PycharmProjects/schoolBell/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/sarah/AppData/Local/Programs/Python/Python311/Lib/site-packages/pystray', 'pystray/'), ('C:/Users/sarah/AppData/Local/Programs/Python/Python311/Lib/site-packages/customtkinter', 'customtkinter/'), ('C:/Users/sarah/PycharmProjects/schoolBell/alarmicon.ico', '.'), ('C:/Users/sarah/PycharmProjects/schoolBell/alarmicon.png', '.'), ('C:/Users/sarah/PycharmProjects/schoolBell/alarms_data.json', '.'), ('C:/Users/sarah/PycharmProjects/schoolBell/alarms_status_data.json', '.'), ('C:/Users/sarah/PycharmProjects/schoolBell/background.png', '.'), ('C:/Users/sarah/PycharmProjects/schoolBell/beep-05.wav', '.'), ('C:/Users/sarah/PycharmProjects/schoolBell/main.spec', '.'), ('C:/Users/sarah/PycharmProjects/schoolBell/new_icon.png', '.'), ('C:/Users/sarah/PycharmProjects/schoolBell/plus.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\sarah\\PycharmProjects\\schoolBell\\alarmicon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
