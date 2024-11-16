import streamlit as st

import ak_sap
from ak_sap import Sap2000Wrapper
from ak_sap.gui.streamlit import st_initialize

st.markdown("## SAP Aid")
st.caption(f"Current Version: {ak_sap.__version__}")
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
            "Error attaching to SAP2000 instance. Maybe try setting path to `SAP2000.exe` below?"
        )
        st.error(e)
        st.session_state["attached"] = False

    try:
        if (
            st.session_state.get("sap_path") is not None
            and st.session_state["sap_path"].strip() != ""
        ):
            st.session_state["SAP"] = Sap2000Wrapper(
                attach_to_exist=True, program_path=st.session_state["sap_path"]
            )
            success_msg()
        else:
            st.session_state["SAP"] = Sap2000Wrapper(attach_to_exist=True)
            success_msg()
    except Exception as e:
        fail_msg(e.__str__())


# <!-----Set custom SAP2000.exe Path-------->
_custom_path = st.checkbox(
    label="Set path to SAP2000.exe?",
    help="Use this if you get error when linking to a SAP2000 Instance.",
    disabled=st.session_state["attached"],
)
if _custom_path:
    st.text_input(
        label="Path to SAP2000.exe",
        key="sap_path",
        placeholder=r"C:\Program Files\Computers and Structures\SAP2000 24\SAP2000.exe",
        disabled=st.session_state["attached"],
    )

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
