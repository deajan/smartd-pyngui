
## smartd-pyngui  [![Build Status](https://travis-ci.org/deajan/smartd_pyngui.svg?branch=master)](https://travis-ci.org/deajan/smartd_pyngui) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/5212dc9547ca4d6e9aafcea945f1fb93)](https://app.codacy.com/app/ozy/smartd_pyngui?utm_source=github.com&utm_medium=referral&utm_content=deajan/smartd_pyngui&utm_campaign=Badge_Grade_Dashboard)

Portable GUI written in python to configure the smart daemon from smartmontools project.
Should write smartd.conf files compatible with every smartmontools release since 5.43
Works on Windows NT 5+, Linux, *BSD (and maybe Mac ?)

Tested with Python 3.6 and 3.7

## Installation

smartd-pyngui needs tkinter PySimpleGUI.
tkinter should be available with a large range of distributions

Example for Redhat / CentOS / Fedora:

for Python3.6.x: ```yum install python36-tkinter```

Example for Debian / Ubuntu / Mint:

for Python 3.x: ```apt-get install python3-tk```

The easyiest way to get PySimpleGUI is using pip.

If not installed, get pip by with the following command:

```wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py```

After that, you may install PySimpleGUI with pip using ```pip install PySimpleGUI```.

## Usage

Run
```python smartd-pyngui.py```

## Executable files

smartd-pyngui may be freezed or compiled after it has been converted to C code.
As of today it has been tested under Windows with py2exe and nuitka.

To freeze and create an executable on windows, install py2exe (via pip) and run ```setup-smartd-pyngui.py```
Executable file will be created in dist directory.

To compile and create an executable on windows, install nuitka (via pip) and run 
```nuitka --standalone --portable smartd-pyngui.py```
Executable file will be created in smart-pyngui.dist directory. Don't forget to add the ui file.

