# ziggy: A Zig Compiler Manager

## Requirements

**ziggy** requires the package ***requests***. To install the requirements follow the steps below :arrow_down:

<details open>
<summary><strong>Unix</strong></summary>

``` bash
# Debian
sudo apt install python-requests

# Fedora
sudo dnf install python-requests

# Arch Linux
sudo pacman -S python-requests

# For other package managers read the documentation for the Python requests package installation
```
</details>

<details open>
<summary><strong>Windows</strong></summary>

``` powershell
pip install requests
```
</details>

## Do It Yourself

<details>
<summary><strong>Options</strong></summary>

```bash
# Download the Github repository
git clone https://gihub.com/sneekyfoxx/ziggy && cd ziggy

# Use Python zippapp on Linux
python3 -m zipapp -o ziggy -p "/usr/bin/env python3" -c pkg
mv ./ziggy location/on/PATH/ziggy

# Use Python's pyinstaller module on Windows
pyinstaller -F -n ziggy .\ziggy\pkg\__main__.py
move .\ziggy c:\Windows\System32\ziggy.exe
```
</details>

## ziggy Usage

<details>
<summary><strong>Options</strong></summary>

```bash
VERSION means **stable** or **master**

ziggy delete   VERSION   # delete the given installed compiler version
ziggy fetch    VERSION   # fetch the given supporting compiler version from the internet
ziggy help               # show help options for ziggy CLI utility
ziggy use      VERSION   # use the supplied version as the default compiler
ziggy upgrade  VERSION   # upgrade the given compiler to the latest version
```
</details>
