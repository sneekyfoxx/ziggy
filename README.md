# ziggy: An Installer and Manager for Zig Compilers

**ziggy** is a dynamically linked Python execuatable binary produced using **pyinstaller**. This means that *ziggy* depends on an installation of Python (Python3 to be exact).

## Requirements

**ziggy** requires the packages ***requests*** and ***BeautifulSoup4***. To install the requirements follow the steps below :arrow_down:

<details open>
<summary><strong>Unix</strong></summary>

On some systems you may have to use your package manager to install the Python **virtualenv** package.

``` bash 
python -m venv ziggy_env    # create a virtual environment
source ./ziggy_env/bin/activate
pip install -r <(curl -s https://raw.githubusercontent.com/sneekyfoxx/ziggy/main/requirements.txt)
deactivate
```
</details>

<details open>
<summary><strong>Windows</strong></summary>

``` powershell
curl -s https://raw.githubusercontent.com/sneekyfoxx/ziggy/main/requirements.txt > requirements.txt
pip install -r requirements.txt
del requirements.txt
```
</details>

## ziggy Usage

<details>
<summary><strong>Options</strong></summary>

```bash
VERSION means **stable** or **master**

ziggy delete   VERSION   # delete the given installed compiler version
ziggy fetch    VERSION   # fetch the given supporting compiler version from the internet
ziggy use      VERSION   # use the supplied version as the default compiler
```
</details>

