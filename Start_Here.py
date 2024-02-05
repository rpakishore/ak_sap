import streamlit as st

from ak_sap import debug, Sap2000Wrapper, log
from ak_sap.gui.streamlit import set_session_state

set_session_state()
st.markdown('## SAP Aid')

def change_debug():
    debug(st.session_state['debug_mode'])
    if st.session_state['debug_mode']:
        st.text_area(label='Log',value=''.join(log.contents()),height=500)
st.toggle('Debug Mode', value=False, key='debug_mode', on_change=change_debug)

def attach_to_model():
    def success_msg():
        st.balloons()
        st.success('Successfully attached to SAP2000 instance')
        
    def fail_msg(e):
        st.error('Error attaching to SAP2000 instance. Maybe try setting path to `SAP2000.exe` below?')
        st.error(e)
    try:
        if st.session_state.get('sap_path') is not None and st.session_state['sap_path'].strip() != "":
            Sap2000Wrapper(attach_to_exist=True, program_path=st.session_state['sap_path'])
            success_msg()
        else:
            Sap2000Wrapper(attach_to_exist=True)
            success_msg()
    except Exception as e:
        fail_msg(e.__str__())

_custom_path = st.checkbox(label='Set path to SAP2000.exe?', help='Use this if you get error when linking to a SAP2000 Instance.')
if _custom_path:
    st.text_input(label='Path to SAP2000.exe', key='sap_path',placeholder=r'C:\Program Files\Computers and Structures\SAP2000 24\SAP2000.exe')

st.button('Attach to Model', on_click=attach_to_model)

