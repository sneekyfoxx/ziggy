# ziggy: An Installer and Manager for Zig Compilers

**ziggy** is a Python zip file (*.pyz/.pyw*) produced using **zipapp**. *zipapp* allows this file to be executed by embedding a header.

## Requirements

**ziggy** require the ***requests*** and ***BeautifulSoup4*** packages. To install the requirements follow the steps below:

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
ziggy list    supported # display the Zig compilers with support for your platform and architecture
ziggy list    installed # display the Zig compilers installed on your system
ziggy install VERSION   # install a specific version of the Zig compiler
ziggy upgrade           # upgrade to the latest Zig compiler version
ziggy primary VERSION   # set a specific (installed) Zig compiler version as the primary version
ziggy destroy VERSION   # remove a specific (installed) Zig compiler version
ziggy version           # display the current 'ziggy' version
```
</details>

