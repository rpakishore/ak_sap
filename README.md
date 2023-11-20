<!--- Heading --->
<div align="center">
  <h1>Template README</h1>
  <p>
    An awesome README template for your projects! 
  </p>
<h4>
    <a href="https://github.com/rpakishore/Template-Python/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/Template-Python">Documentation</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/Template-Python/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/Template-Python/issues/">Request Feature</a>
  </h4>
</div>
<br />

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/rpakishore/Template-Python)
![GitHub last commit](https://img.shields.io/github/last-commit/rpakishore/Template-Python)
<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
  - [1.1. Screenshots](#11-screenshots)
  - [1.2. Features](#12-features)
  - [1.3. Environment Variables](#13-environment-variables)
- [2. Getting Started](#2-getting-started)
  - [2.1. Prerequisites](#21-prerequisites)
  - [2.2. Dependencies](#22-dependencies)
  - [2.3. Installation](#23-installation)
    - [2.3.1. Production](#231-production)
    - [2.3.2. Development](#232-development)
- [3. Usage](#3-usage)
  - [3.1. Development](#31-development)
- [4. Roadmap](#4-roadmap)
- [5. FAQ](#5-faq)
- [6. License](#6-license)
- [7. Contact](#7-contact)
- [8. Acknowledgements](#8-acknowledgements)

<!-- About the Project -->
## 1. About the Project
<!-- Screenshots -->
### 1.1. Screenshots

<div align="center"> 
  <img src="https://placehold.co/600x400?text=Your+Screenshot+here" alt="screenshot" />
</div>

<!-- Features -->
### 1.2. Features

- Feature 1
- Feature 2
- Feature 3

<!-- Env Variables -->
### 1.3. Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`

<!-- Getting Started -->
## 2. Getting Started

<!-- Prerequisites -->
### 2.1. Prerequisites

Python 3.11 or above

### 2.2. Dependencies

Create the virutual environment and install dependencies

```bash
python -m venv .venv

.venv\Scripts\activate.bat

pip install flit
```

<!-- Installation -->
### 2.3. Installation

#### 2.3.1. Production

Install with flit

```bash
  flit install --deps production
```

#### 2.3.2. Development

Download the git and install via flit

```bash
git clone https://github.com/rpakishore/ak_pdf.git
cd ak_pdf
pip install flit
flit install
```

<!-- Usage -->
## 3. Usage

```python
from template_python import Reader, debug
debug(True) #For debug messages, Can be skipped.

# Initialize
pdf = Reader(filepath=r"textbook.pdf", password=None)
```

### 3.1. Development

1. Open the project directory in vscode
2. Update the app name under `pyproject.toml`
3. Change the folder name from `src\template_python` to `src\<app_name>`, and propate the changes to the subfolders.
4. Review the dependencies under `pyproject.toml` and remove as needed.
5. Remove unneeded dependencies from `src\<app_name>\`

<!-- Roadmap -->
## 4. Roadmap

- [x] Set up a skeletal framework
- [ ] Todo 2

<!-- FAQ -->
## 5. FAQ

- Question 1
  - Answer 1

- Question 2
  - Answer 2

<!-- License -->
## 6. License

See LICENSE for more information.

<!-- Contact -->
## 7. Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/Template-Python](https://github.com/rpakishore/Template-Python)

<!-- Acknowledgments -->
## 8. Acknowledgements

- [Awesome README Template](https://github.com/Louis3797/awesome-readme-template/blob/main/README-WITHOUT-EMOJI.md)
- [Shields.io](https://shields.io/)