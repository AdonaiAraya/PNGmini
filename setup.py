from cx_Freeze import setup, Executable

includefiles = ["keys.json", "PNGmini_logo16x16.ico", "PNGmini_logo32x32.ico", "PNGmini_logo64x64.ico", "PNGmini_logo128x128.ico", "PNGmini_logo_ayuda.gif", "README.md"]

setup(
    name = "PNGmini",
    version = "0.5",
    description = "Aplicación de escritorio realizada en python para comprimir imágenes PNG sin perdida de calidad",
    author = "Adonai Araya",
    author_email = "adoargu@gmail.com",
    url = "http://www.doblea.nom.es",
    options = {
        "build_exe":{
            "include_files" : includefiles
        }},
    executables = [
        Executable(
            "main.py",
            base = "Win32GUI",
            shortcutName = "PNGmini",
            shortcutDir = "DesktopFolder",
            icon = "PNGmini_logo128x128.ico"
        )
    ]
)
