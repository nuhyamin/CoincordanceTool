import os
import sys
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Users\ACER\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\ACER\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('texteditor.py', base=base, icon="dictionary.ico")
]

setup(name='NYConc 0.1',
      version='0.1',
      options={"build_exe":{"packages":["wx"],"include_files":["dictionary.ico", "Fiction"]}},
      description='Concordance tool',
      executables=executables
      )