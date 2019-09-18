from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name="Korean Dictionary Tester",
    options=options,
    version="0.001",
    description='Test build of KDT',
    executables=executables
)
