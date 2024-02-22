from hilti_profis import PE
import streamlit as st

from datetime import datetime
import os
import tempfile

from ak_sap import Sap2000Wrapper

def main():
    sap:Sap2000Wrapper = st.session_state['SAP']
    _steps = """
    Steps to follow:
    1. Run the Analysis on SAP2000.
    2. Select the frame and attached support for export in the 3D model.
    3. Click the `Extract Values` button below.
    """
    st.info(_steps, icon='ℹ️')
    
    if st.session_state.get('_hilti_values_extracted') is None:
        st.session_state['_hilti_values_extracted'] = False
        
    def _hilti_extract_values():
        try:
            st.session_state['_hilti_values_extracted'] = sap.Element.Point.selected().__next__()
        except StopIteration:
            st.session_state['_hilti_values_extracted'] = None
            st.warning('Make sure the node is selected.')
        
    st.button('Extract Values', on_click=_hilti_extract_values)
    
    @st.cache_data
    def load_hilti_class(basefile):
        return PE(basefile=basefile)
    
    if st.session_state['_hilti_values_extracted']:
        try:
            selected_section = sap.Element.Frame.get_section(frame_name=sap.Element.Frame.selected().__next__())
        except StopIteration:
            selected_section = None

        st.divider()
        st.markdown('##### Selections')
        _lcases = sap.Load.Case.list_all()
        _lcombos = sap.Load.Combo.list_all()
        
        col1, col2, col3 = st.columns(3)
        cases = col1.multiselect(label='Load Cases for Export', default=_lcases, options=_lcases)
        combos = col2.multiselect(label='Load Combos for Export', default=_lcombos, options=_lcombos)
        #col3.write(f'##### Selected Section: \n###### {selected_section}')
        col3.table(data = {'Selected Section':selected_section, 'Selected Node #':st.session_state['_hilti_values_extracted']})
        
        col1, col2 = st.columns([3,1])
        uploaded_file = col2.file_uploader(
            label = 'Upload a base `.pe` file (Optional)',
            accept_multiple_files=False,
            help='You can optionally provide a `.pe` file as reference. All other design values will be imported from supplied file',
            key = 'pe_basefile',
            type='pe'
        )
        
        col1, col2, col3 = col1.columns(3)
        _axis = [1,2,3]
        x_axis = col2.selectbox(label='X-axis', options=_axis, index=0)
        y_axis = col3.selectbox(label='Y-axis', options=_axis, index=1)
        z_axis = col1.selectbox(label='Z-axis', options=_axis, index=2)

        def generate_pe() -> str:
            sap:Sap2000Wrapper = st.session_state['SAP']
            if not x_axis != y_axis != z_axis:
                st.error('^ Make sure X, Y, Z axis are mutually exclusive from each other')
            if uploaded_file is not None:
                basefile = os.path.join(tempfile.mkdtemp(), uploaded_file.name)
                with open(basefile, "wb") as f:
                    f.write(uploaded_file.getvalue())
            else:
                basefile = None
            anchor = load_hilti_class(basefile=basefile)
            
            sap.Results.Setup.clear_casecombo()
            
            for case in cases:
                sap.Results.Setup.select_case(casename=case)
            
            for combo in combos:
                sap.Results.Setup.select_combo(comboname=combo)
            
            _current_units = sap.Model.units
            sap.Model.set_units(value="N_mm_C")
            
            #Delete Existing Load Combinations
            anchor.Model.Loads.Combos.data['LoadCombinationEntity'] = None
            
            for rxn in sap.Results.joint_reactions(jointname=st.session_state['_hilti_values_extracted']):
                anchor.Model.Loads.Combos.add(
                    Fx=-rxn[f"F{x_axis}"],
                    Fy=-rxn[f"F{y_axis}"],
                    Fz=-rxn[f"F{z_axis}"],
                    Mx=-rxn[f"M{x_axis}"],
                    My=-rxn[f"M{y_axis}"],
                    Mz=-rxn[f"M{z_axis}"],
                    LoadType='Seismic',
                    Comment=rxn["LoadCase"]
                )
            sap.Model.set_units(value=_current_units)
            
            anchor.Model.apply()
            _xml=anchor.xml_content() 
            assert isinstance(_xml, str)
            return anchor.xml_content() # type: ignore
        
        st.divider()
        
        # Todo
        # Defer the `generate_pe` function run until the button is clicked.
        # Currently on [streamlit roadmap](https://roadmap.streamlit.app) for May-July ("Deferred data load for st.download_button")
        st.download_button(
            label='Export `.pe` file',
            data=generate_pe(),
            file_name=f"{sap.Model.filepath.stem}-{st.session_state['_hilti_values_extracted']}{'-'+selected_section if selected_section else ''}-AK-{datetime.now():%m%d_%H%M}.pe", 
            type='primary',
            mime = 'text/plain'
        )
