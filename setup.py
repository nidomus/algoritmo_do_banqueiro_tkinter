from cx_Freeze import setup, Executable
setup(
    name = "Algoritmo do Banqueiro",
    version = "1.0.0",
    options = {"build_exe": {
        'packages': ["Algoritmo","ttkbootstrap"],
        'include_files': ['ifba.ico'],
        'include_msvcr': True,
    }},
    executables = [        Executable(
            "simulador.py",
            copyright="Copyright (C) 2022 cx_Freeze",
            base="Win32GUI",
            icon="ifba.ico",
            shortcutName="Simulador",
            shortcutDir="DesktopFolder"
            )]
    )
