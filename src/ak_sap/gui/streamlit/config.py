import streamlit as st

DEFAULT_SESSION_STATES = {
    'attached': False,
    'debug_mode': False
}
def set_session_state(values: dict=DEFAULT_SESSION_STATES, force: bool=False):
    for k, v in values.items():
        if force or st.session_state.get(k) is None:
            st.session_state[k] = v