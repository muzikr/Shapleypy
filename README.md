# Shapleypy
A python library for cooperative game theory


[![PyPI - Version](https://img.shields.io/pypi/v/Shapleypy.svg)](https://pypi.org/project/Shapleypy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Shapleypy.svg)](https://pypi.org/project/Shapleypy)
![Test](https://github.com/muzikr/Shapleypy/actions/workflows/test-master.yml/badge.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

-----

**Table of Contents**

- [Shapleypy](#shapleypy)
  - [Installation](#installation)
    - [Linux](#linux)
    - [MacOS](#macos)
    - [Windows](#windows)
  - [License](#license)


## Installation

To install latest stable version use:

```console
pip install shapleypy
```
To install latest development version use:

```console
pip install -i https://test.pypi.org/simple/ shapleypy
```

### Linux

To install this package for Linux you need to set ```$CPPFLAGS``` to contain ```-std=c++11```. This can be achieve by

```bash
export CPPFLAGS="-std=c++11 $CPPFLAGS"
```
> [!NOTE]
> We know that ```CPPFLAGS``` are not meant for C++, but ```CXXFLAGS``` are not suported by setuptools.

or by running the installation in form of

```bash
CPPFLAGS="-std=c++11" pip install shapleypy
```
not to make the standart pernament.

Also there are some non-python dependencies. Those could be installed via distribution package manager.

Ubuntu:
```bash
sudo apt-get install -y ppl-dev libgmp-dev libmpfr-dev libmpc-dev
```


### MacOS

> [!WARNING]
> Convex game generator is currently not available for MacOS

There are some non-python requirements. These could be installed via homebrew:

```bash
brew install ppl gmp mpfr libmpc
```

> [!NOTE]
> If you installed those dependencies via ```brew``` as shown you probably also will need to set paths of libraries installed by ```brew``` for clang:
> ```export CFLAGS="-I/opt/homebrew/include/ -L/opt/homebrew/lib/ -I/opt/homebrew/include/ -L/opt/homebrew/lib $CFLAGS"```

### Windows

> [!WARNING]
> Convex game generator and core solution concept are currently not available for Windows

## License

`Shapleypy` is distributed under the terms of the [GPL-3.0](https://spdx.org/licenses/GPL-3.0-or-later.html) license.
