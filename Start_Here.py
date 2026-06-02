from pathlib import Path

import streamlit as st
import tomllib

from ak_sap import Sap2000Wrapper
from ak_sap.gui.streamlit import st_initialize

st.markdown("## SAP Aid")
with open(Path(__file__).parent / "pyproject.toml", "r") as f:
    config = tomllib.loads(f.read())
st.caption(f"Current Version: {config['project']['version']}")
_disclaimer = """
ℹ **Important Information**   
- Features of this GUI is **heavily limited** compared to the base package.
- This GUI only serves to demonstrate possibilities with the `ak_sap` wrapper itself.
"""
st.info(_disclaimer)


st_initialize()


st.toggle("Debug Mode", value=False, key="debug_mode")


def attach_to_model():
    def success_msg():
        st.balloons()
        st.success("Successfully attached to SAP2000 instance")
        st.session_state["attached"] = True

    def fail_msg(e):
        st.error(
            "Error attaching to SAP2000 instance. Make sure SAP2000 (v17 or newer) is running with a model open."
        )
        st.error(e)
        st.session_state["attached"] = False

    try:
        st.session_state["SAP"] = Sap2000Wrapper(attach_to_exist=True)
        success_msg()
    except Exception as e:
        fail_msg(e.__str__())


# <!-----Attach to SAP button-------->
st.button(
    "Attach to Model", on_click=attach_to_model, disabled=st.session_state["attached"]
)

if st.session_state["SAP"] is None:
    st.stop()

sap: Sap2000Wrapper = st.session_state["SAP"]
st.divider()
with st.expander("File Info"):
    st.table(
        {
            "App Version #": sap.version,
            "API Version #": sap.api_version,
            "Current Filepath": sap.Model.filepath,
        }
    )
with st.expander("Project Info"):
    st.table({k: v for k, v in sap.Model.project_info.items() if v != ""})
st.divider()
