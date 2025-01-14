import streamlit as st

from ak_sap import Sap2000Wrapper
from ak_sap.gui.streamlit import st_initialize

st.write("## Tables")
st_initialize()

if not st.session_state.get("attached"):
    st.warning("[Attach to existing](/) SAP model first to use this tab")
    st.stop()

sap: Sap2000Wrapper = st.session_state["SAP"]
st.divider()
with st.expander("Tables Tables"):
    _all = st.checkbox("Show All")
    if _all:
        st.table(sap.Table.list_all())
    else:
        st.table(sap.Table.list_available())
st.divider()
