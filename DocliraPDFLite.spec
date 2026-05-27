# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ["run.py"],
    pathex=[],
    binaries=[],
    datas=[("assets/doclira_lite.ico", "assets")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="DocliraPDFLite",
    icon="assets/doclira_lite.ico",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)
