- [Installation](#installation)
- [Usage](#usage)
  - [Attach an Instance](#attach-an-instance)
  - [Models](#models)
  - [Tables](#tables)
  - [Export](#export)
    - [Hilti-Profis](#hilti-profis)

<h1> Steamlit </h1>

**Please note, the GUI is currently heavily limited in functionality and only serves to showcase the possibilities with the ak_sap module.**

The base `ak_sap` does not comes pre-compiled with the streamlit package.

You will need to use the `--extra gui` command during install to add the streamlit package.

# Installation

```cmd
git clone https://github.com/rpakishore/ak_sap.git && cd ak_sap
pip install uv
uv venv && uv pip install -r pyproject.toml --extra gui
```

# Usage

- Make sure the SAP Model you want to control is open. (Current version of gui does not support creating new SAP files)

```cmd
uv run streamlit run Start_Here.py
```

- Open up the SAP2000 model of your choice and click `Attach to Model`

## Attach an Instance

![GUI-Streamlit-Start_Here.png](../assets/GUI-streamlit-Start_Here.png)

## Models

![GUI-Streamlit-Models.png](../assets/GUI-streamlit-Models.png)

## Tables

![GUI-Streamlit-Tables.png](../assets/GUI-streamlit-Tables.png)

## Export

![GUI-streamlit-Export.png](../assets/GUI-streamlit-Export.png)

### Hilti-Profis

![GUI-streamlit-Export-Hilti.png](../assets/GUI-streamlit-Export-Hilti.png)

Steps:

1. Run the Analysis on SAP2000
2. Select the frame and attached support point for export from the 3D model.
3. Click the `Extract Values` button in browser.
4. Select the interested load combinations and cases for export.
5. Orient the Axis, by assigning `X`, `Y`, `Z` axis of Hilti to axis `1`(Red), `2` (Green) and `3`(Blue) of SAP.
6. Optionally, upload an exisitng `.pe` file to import default values.
7. Click the `Export .pe file` button.
8. The exported file will be of format "`SAP filename`-`Selected Node #`-`Selected Section Shape`-`MMDD`_`HHMM`.pe"

To Implement:

- [ ] Incorporate the section profile into the `.pe` file.
- [ ] Replace the manual deletion of existing loadcase with inbuilt `delete_existing` method of Hilti-Profis Class in version `0.0.4`.
- [ ] Defer data generation until the click of download button (Part of Streamlit roadmap for May-July 2024).