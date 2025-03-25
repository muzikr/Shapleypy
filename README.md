# Shapleypy
A python library for cooperative game theory


[![PyPI - Version](https://img.shields.io/pypi/v/shapleypy.svg)](https://pypi.org/project/shapleypy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shapleypy.svg)](https://pypi.org/project/shapleypy)
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
To install latest development version you can clone the repository and use hatch (must be installed) to create an enviroment containg latest dev version:

```console
hatch shell
```

or build the project and install it to whatever enviroment you want:

```bash
hatch build
# the wheel will be located in dist directory
pip install $PATH_TO_WHEEL_FILE
```

<!--
```console
pip install -i https://test.pypi.org/simple/ shapleypy
```
-->

### Linux


Few non-python dependencies have to be installed prior the installation of the __Shapleypy__. Those could be installed via distribution package manager.

Ubuntu:
```bash
sudo apt-get install -y ppl-dev libgmp-dev libmpfr-dev libmpc-dev
```


### MacOS

There are some non-python requirements. These could be installed via homebrew:

```bash
brew install ppl gmp mpfr libmpc
```

> [!NOTE]
> If you installed those dependencies via ```brew``` as shown you probably also will need to set paths of libraries installed by ```brew``` for clang:
> ```export CFLAGS="-I/opt/homebrew/include/ -L/opt/homebrew/lib/ -I/opt/homebrew/include/ -L/opt/homebrew/lib $CFLAGS"```

### Windows

> [!WARNING]
> The core solution concept is currently not available for Windows.

## License

`Shapleypy` is distributed under the terms of the [GPL-3.0](https://spdx.org/licenses/GPL-3.0-or-later.html) license.
