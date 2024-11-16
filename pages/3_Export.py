import importlib.machinery
import importlib.util
from pathlib import Path

import streamlit as st

from ak_sap.gui.streamlit import st_initialize


def load_module_main(filename: str):
    """Specifying the python filename under the /pages/windows folder, loads the main() function from specified file.

    Args:
        filename (str): python filename to load the function from
    """
    abs_path = Path(__file__).parent / "Export" / filename
    loader = importlib.machinery.SourceFileLoader(abs_path.stem, str(abs_path))
    spec = importlib.util.spec_from_loader(abs_path.stem, loader)
    mymodule = importlib.util.module_from_spec(spec)  # type: ignore
    loader.exec_module(mymodule)
    mymodule.main()


st.set_page_config(layout="wide")

st.write("## Export")
st_initialize()

if not st.session_state.get("attached"):
    st.warning("[Attach to existing](/) SAP model first to use this tab")
    st.stop()

with st.expander("Export to Hilti-Profis"):
    load_module_main("hilti_export.py")
