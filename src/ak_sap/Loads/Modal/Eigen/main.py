from ak_sap.utils.decorators import smooth_sap_do

class Eigen:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
    
    def __str__(self) -> str:
        return f'Instance of `Loads.Modal.{self.__class__.__name__}`. Holds collection of functions'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @smooth_sap_do
    def get_initial_case(self, case_name: str) -> str:
        """retrieves the initial condition assumed for the specified load case.
        
        Response: This is blank, None, or the name of an existing analysis case. 
        This item specifies if the load case starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time history load case.
        If the specified initial case is a nonlinear static or nonlinear direct integration time history load case, the stiffness at the end of that case is used. 
        If the initial case is anything else, zero initial conditions are assumed.
        """
        return self.SapModel.LoadCases.ModalEigen.GetInitialCase(case_name)
    
    @smooth_sap_do
    def set_initial_case(self, case_name: str, initial_case: str):
        """sets the initial condition for the specified load case.
        `initial_case` lets you use stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time history load case.
        """
        return self.SapModel.LoadCases.ModalEigen.SetInitialCase(case_name, initial_case)
    
    @smooth_sap_do
    def get_loads(self, case_name: str) -> dict:
        """ retrieves the load data for the specified load case."""
        _ret: tuple = self.SapModel.LoadCases.ModalEigen.GetLoads(case_name)
        _values: dict = {
            'NumberOfLoads': _ret[0],
            'LoadType': _ret[1],
            'LoadName': _ret[2],
            'Target Participation Ratio': _ret[3],
            'Calculate Static Correction Modes': True if _ret[4] == 1 else False
        }
        return _values, 0 # type: ignore
    
    @smooth_sap_do
    def get_number_modes(self, case_name: str) -> tuple[int]:
        """retrieves the number of modes requested for the specified load case."""
        return self.SapModel.LoadCases.ModalEigen.GetNumberModes(case_name)
    
    @smooth_sap_do
    def set_number_modes(self, case_name: str, max: int, min: int):
        """sets the number of modes requested for the specified load case."""
        return self.SapModel.LoadCases.ModalEigen.SetNumberModes(case_name, max, min)
    
    @smooth_sap_do
    def get_parameters(self, case_name: str):
        """retrieves various parameters for the specified load case."""
        _ret: tuple = self.SapModel.LoadCases.ModalEigen.GetParameters(case_name)
        _values: dict = {
            'EigenShiftFreq': _ret[0],
            'EigenCutOff': _ret[1],
            'EigenTolerance': _ret[2],
            'AllowAutoFreqShift': True if _ret[3] == 1 else False
        }
        return _values, 0 # type: ignore
    
    @smooth_sap_do
    def set_parameters(self, case_name: str, EigenShiftFreq: float, EigenCutOff: float, 
                        EigenTolerance: float, AllowAutoFreqShift: bool):
        """sets various parameters for the specified modal eigen load case."""
        return self.SapModel.LoadCases.ModalEigen.GetParameters(case_name, EigenShiftFreq, 
                                                                EigenCutOff, EigenTolerance, int(AllowAutoFreqShift))
    
    @smooth_sap_do
    def set_case(self, case_name: str):
        """Initializes a modal eigen load case. 
        If this function is called for an existing load case, all items for the case are reset to their default value"""
        return self.SapModel.LoadCases.ModalEigen.SetCase(case_name)