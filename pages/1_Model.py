import streamlit as st
from ak_sap.gui.streamlit import st_initialize
from ak_sap import Sap2000Wrapper

st.write('## Models')
st_initialize()

if not st.session_state.get('attached'):
    st.warning('[Attach to existing](/) SAP model first to use this tab')
    st.stop()

sap:Sap2000Wrapper = st.session_state['SAP']
st.divider()
with st.expander('Model Info'):
    st.table(
        {'Current Model Units':sap.Model.units.replace('_', ' | '),
        'Current Database Units':sap.Model.units_database.replace('_', ' | '),
        'Merge Tolerance': sap.Model.merge_tol,
        'Is Locked': sap.Model.is_locked
        })
st.divider()