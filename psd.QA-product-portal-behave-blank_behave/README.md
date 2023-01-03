# Install & Setup Environment

NOTE: For install/setup script: https://confluence.rsi.lexisnexis.com/display/SDEITG/Python+Dev+Environment+Setup


**_1:_** Clone the Project

  - Clone this project using Github Desktop  

**_2:_** Download and Install the latest version of VS Code

- 2.1: Click Windows Key, type Powershell, click Enter
- 2.2: type `code`, click Enter
- 2.3: **App launches **
- 2.4: Click 'Help', Click 'Check For Updates'

**_3:_** Download and Install the latest version of Python

- 3.1: Click Windows Key, type Powershell, click Enter
- 3.2: type `python`, click Enter
- 3.3: **Relx Business Store App launches ** (If you can't download python from app store, use this guide to setup Python: https://confluence.rsi.lexisnexis.com/display/SDEITG/Python+Setup)
- 3.4: Click 'Install' for Python 3.9

Update environment variable 'Path' to include the location of python installation: `C:\Users\<risk_user>\AppData\Local\Microsoft\WindowsApps`

You can find Guide to updating Environment Variable 'Path' here: `https://www.computerhope.com/issues/ch000549.htm`

**_4:_** Install or Update pip

You can find Installation Guide to your system here: https://pypi.org/project/pip/

- `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

You might need to update environment variable Path to include the location of pip installation: `C:\Users\<risk_user>\AppData\Local\Programs\Python\Python39\Scripts`

**_5:_** Install behave and all dependencies listed on requirements.txt inside your project

From Terminal (ie. GitBash, powershell, vscode):

Execute these commands:

- `cd ~/git/python-bdd-framework`
- `pip install -r requirements.txt`

**_6:_** Install VS Code Extensions:  

  - From VS Code, go to Extensions `View -> Extensions`
  - Type `Python` in the 'Search Extensions in Marketplace' box; Click the first one; Click Install
  - Type `Cucumber (Gherkin) Full Support` in the 'Search Extensions in Marketplace' box; Click the first one; Click Install
  - Type `Behave Test Explorer` select the version `0.0.1` and click install


**_Install apropriate webdrivers:_** 

Download links for your webdrivers:

| Browser  | Link                                                                  |
| -------- | --------------------------------------------------------------------- |
| Chrome:  | https://sites.google.com/a/chromium.org/chromedriver/downloads        |
| Edge:    | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ |
| Firefox: | https://github.com/mozilla/geckodriver/releases                       |

Once downloaded, webdrivers can be relocated (copied) to `C:\Users\<risk_user>\AppData\Local\Microsoft\WindowsApps`


**VS Code User Settings**

  
  **_1:_** Open VS Code
  
  **_2:_** Click 'File', Click 'Open Folder', Navigate to 'C:\Users\<risk id>\git', select 'PYTHON-BDD-FRAMEWORK'
  
  **_3:_** Go to Command Palette `View -> Command Palette`
  
  **_4:_** Type `Open settings (JSON)`, Click the first option
  
  **_5:_** Copy the contents of `sample_settings.txt` and replace it inside settings.json, update `python.pythonPath` with your path; save
  
  **_6:_** From Explorer (Left-hand side), Right-Click `context`, create `New File`, name it `testsettings.json`
  
  **_7:_** Copy the contents of `sample_testsettings.txt` to your new `testsettings.json`; save
  
  **_8:_** restart VS Code
  
  *Note: If setup was successful, from VS Code Terminal, you should be able to run the test 
  - `cd ~/git/python-bdd-framework`
  - `behave`

  *Tools to help define locators: `https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl?hl=en`


**Test Execution Examples:**

- `behave features/FAT/login.feature`
- `behave features/FAT/login.feature features/home.feature`
- `behave --no-capture -D environment=desenv -D browser=firefox --tags=@wip features_path/feature_name.feature`  

## Allure Reports

**Pre-requisite**

1. Install Allure-Behave 

   `pip install allure-behave`

2. Install Allure 

   `scoop install allure`
   
    If you don't have scoop installed run this command from powershell
    
    `iwr -useb get.scoop.sh | iex`
    
    `If you receive the message "PowerShell requires an execution policy in [Unrestricted, RemoteSigned, ByPass] to run scoop type the following:
    Set-ExecutionPolicy RemoteSigned -scope CurrentUser. Once complete, execute iwr -useb get.scoop.sh _ iex`


Allore installation guide: https://docs.qameta.io/allure/#_installing_a_commandline

To verify installation run below command:

`scoop update allure`

**Generate Report**

Execute test and generate report files (.json) and files will be hosted ` -o reports/` directory.

 `behave -f allure_behave.formatter:AllureFormatter -o reports/ features/FAT/login.feature`

Generate Allure Report

 `allure serve reports/`

Documentation:  https://docs.qameta.io/allure/#_behave

**User Guide of Behave Framework:**

You can find information about behave framework here: https://behave.readthedocs.io/en/latest/

To change the environment use -D environment=SOME*ENVIRONMENT like command line below from Terminal:

The default environment is always define by behave.ini*

- `python -m behave -D environment=homolog`
   Note: if `python` does not execute the command, try `py` instead

For change the browser use -D browser=SOME*BROWSER like command line below:

The default browser is always define by behave.ini*

- `python -m behave -D browser=headless-chrome`

To execute a specific feature execute the command line:

- `python -m behave features_path/feature_name.feature`

By default, behave captures stdout, this captured output is only shown if a failure occurs.

To print output execute the command line:

- `python -m behave --no-capture`

You can combine the command lines to execute your test

# Framework Architecture

```powershell
[Root Directory]
\-- context
    \-- config.py
    \-- driver.py
    \-- testsettings.json
\-- features
    \-- environment.py
    \-- product
        \-- Login
            -- .feature
        \-- Misc
        \-- Report
        \-- Search
\-- pages
    \-- page.py
    \-- product
        \-- Login
            -- page objects
        \-- Misc
        \-- Report
        \-- Search
        \-- locators.py
\-- steps
    \-- common.py
    \-- product_step definitions
\-- requirements.txt
\-- sample_settings.txt
\-- sample_testsettings.txt
```

**context**

Settings and driver instantiation. This project uses a singleton pattern to represent a webdriver.

**features**

Contains .feature files. These are text files conforming to gherkin syntax.

**pages**

Contains all page objects, as well as locators for finding elements on the webpages.

**steps**

Contains files with test methods which are bound to steps in the .feature files.

**requirements.txt** 

Contains environmental controls for the behave framework.

**environment.py** 

Contains dependencies.

  - `pip install -r requirements.txt`
