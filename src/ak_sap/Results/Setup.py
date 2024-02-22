
from ak_sap.utils import log, MasterClass
from ak_sap.utils.decorators import smooth_sap_do

class ResultsSetup(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        self.Setup = mySapObject.SapModel.Results.Setup
    
    @smooth_sap_do
    def clear_casecombo(self):
        """deselects all load cases and response combinations for output."""
        return self.Setup.DeselectAllCasesAndCombosForOutput()
    
    def is_selected_case(self, casename: str):
        """checks if an load case is selected for output."""
        return self.Setup.GetCaseSelectedForOutput(casename)
    
    def select_case(self, casename: str):
        """sets an load case selected for output flag."""
        return self.Setup.SetCaseSelectedForOutput(casename)
    
    def is_selected_combo(self, comboname: str):
        """checks if an load combo is selected for output."""
        return self.Setup.GetComboSelectedForOutput(comboname)
    
    def select_combo(self, comboname: str):
        """sets an load combo selected for output flag."""
        return self.Setup.SetComboSelectedForOutput(comboname)
    
    def base_rxn_loc_get(self):
        """retrieves the global coordinates of the location at which the base reactions are reported."""
        *coord, _ret = self.Setup.GetOptionBaseReactLoc()
        return {'x':coord[0], 'y':coord[1], 'z':coord[2]}, _ret
    
    def set_rxn_loc_get(self, x: float, y: float, z: float):
        """sets the global coordinates of the location at which the base reactions are reported."""
        return self.Setup.SetOptionBaseReactLoc(x, y, z)
