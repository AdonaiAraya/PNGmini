from cx_Freeze import setup, Executable

includefiles = ["keys.json"]

setup(
    name = "PNGmini",
    version = "0.1",
    description = "test",
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
            shortcutDir = "DesktopFolder"
        )
    ]
)
