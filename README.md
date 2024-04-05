<!--- Heading --->
<div align="center">
  <h1>ak_sap</h1>
  <p>
    Python wrapper for SAP2000. 
    Generate/Analyze/Extract complex structural models using python. 
  </p>
<h4>
    <a href="https://github.com/rpakishore/ak_sap/blob/main/documentation/Usage/GUI.md">GUI</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_sap/tree/main?tab=readme-ov-file#2-getting-started">Getting Started</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_sap/blob/main/documentation/Layout.md">Layout Documentation</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_sap/issues/">Report Bug/Request Feature</a>

  </h4>
</div>
<br />

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/rpakishore/ak_sap)
![GitHub last commit](https://img.shields.io/github/last-commit/rpakishore/ak_sap)
[![tests](https://github.com/rpakishore/ak_sap/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/rpakishore/ak_sap/actions/workflows/test.yml)

<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
- [2. Getting Started](#2-getting-started)
  - [2.1. Prerequisites](#21-prerequisites)
  - [2.2. Installation](#22-installation)
    - [2.2.1. Production](#221-production)
      - [2.2.1.1. Install directly from repo](#2211-install-directly-from-repo)
      - [2.2.1.2. Install from Pypi release](#2212-install-from-pypi-release)
    - [2.2.2. Development](#222-development)
- [3. Usage](#3-usage)
  - [3.1. GUI](#31-gui)
  - [3.2. Layout Documentation](#32-layout-documentation)
- [4. Roadmap](#4-roadmap)
- [5. License](#5-license)
- [6. Contact](#6-contact)
- [7. Acknowledgements](#7-acknowledgements)

<!-- About the Project -->
## 1. About the Project

<!-- Getting Started -->
## 2. Getting Started

<!-- Prerequisites -->
### 2.1. Prerequisites

1. Python 3.11 or above
2. SAP2000 v24 or higher

<!-- Installation -->
### 2.2. Installation

#### 2.2.1. Production

##### 2.2.1.1. Install directly from repo

Clone repo and Install with flit

```bash
git clone https://github.com/rpakishore/ak_sap.git
cd  ak_sap
pip install flit
```

- If you want just the base package:
  
  ```bash
  flit install --deps production
  ```

- Alternatively, if you also want to include the optional streamlit gui:
  
  ```bash
  flit install --deps production --extras gui
  ```

##### 2.2.1.2. Install from Pypi release

```bash
pip install ak_sap
```

Note: The Pypi version does not ship with the optional streamlit gui

#### 2.2.2. Development

Download the git and install via flit

```bash
git clone https://github.com/rpakishore/ak_sap.git
cd  ak_sap
pip install flit
flit install --pth-file
```

Updating Docs:

- Update the [Usage.ipynb](./documentation/Usage.ipynb).
- Open `cmd.exe` to run

  ```bash
  update-doc
  ```

<!-- Usage -->
## 3. Usage

Initialize the module as below

```python
from ak_sap import debug, Sap2000Wrapper
debug(status=False)

#Initialize
sap = Sap2000Wrapper(attach_to_exist=True)      #Attach to existing opened model
sap = Sap2000Wrapper(attach_to_exist=False)     #Create new blank model from latest SAP2000

## Create blank model from a custom version of SAP2000
sap = Sap2000Wrapper(attach_to_exist=False, program_path=r'Path\to\SAP2000.exe')

```

Parent level methods and attributes

```python
sap.hide()                                  #Hide the SAP2000 window
sap.unhide()                                #Unhides SAP2000 window
sap.version                                 #Returns SAP2000 version number
sap.api_version                             #Returns Sap0API version number

sap.save(r'\Path\to\save\file.sdb')
```

### 3.1. GUI

The repo has an optional streamlit GUI for the wrapper. Checkout [`GUI.md`](/documentation/Usage/GUI.md) for installation and usage instructions.

### 3.2. Layout Documentation

To see module level usage, check out the [`Layout.md`](/documentation/Layout.md) or [`Usage.ipynb`](/documentation/Usage.ipynb)

<!-- Roadmap -->
## 4. Roadmap

- [x] Generate Load Patterns
- [x] Generate Load Cases
- [ ] Apply Loads
  - [ ] Points
  - [ ] Area
  - [ ] Line
- [x] Export joint reactions to Hilti-Profis file

<!-- License -->
## 5. License

See [LICENSE](https://github.com/rpakishore/ak_sap/blob/main/LICENSE) for more information.

<!-- Contact -->
## 6. Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/ak_sap](https://github.com/rpakishore/ak_sap)

<!-- Acknowledgments -->
## 7. Acknowledgements

- [Shields.io](https://shields.io/)
