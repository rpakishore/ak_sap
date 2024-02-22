import streamlit as st
from ak_sap import debug, log, Sap2000Wrapper

DEFAULT_SESSION_STATES = {
    'attached': False,
    'debug_mode': False,
    'SAP': None
}
def set_session_state(values: dict=DEFAULT_SESSION_STATES, force: bool=False):
    for k, v in values.items():
        if force or st.session_state.get(k) is None:
            log.debug(f'[STREAMLIT] setting session state variables: {k}={v}')
            st.session_state[k] = v
            
def st_initialize():
    set_session_state()
    debug(st.session_state['debug_mode'])
    if st.session_state['debug_mode']:
        with st.expander('Log Contents'):
            st.text_area(label='Log',value=''.join(log.contents()),height=250)

        sap:Sap2000Wrapper|None = st.session_state.get('SAP')
        if sap is not None:
            with st.expander('Program Logs'):
                st.text_area(label='Log',value=sap.Model.logs)
        