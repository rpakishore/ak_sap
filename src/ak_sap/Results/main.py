
from ak_sap.utils import log, MasterClass
from ak_sap.utils.decorators import smooth_sap_do

class Results(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        self.Results = mySapObject.SapModel.Results
    
    @smooth_sap_do
    def joint_reactions(self, jointname:str) -> dict:
        loads: list[dict] = []
        _, Obj, Elm, LoadCase,StepType, StepNum, F1, F2, F3, M1, M2, M3, ret = self.Results.JointReact(jointname, 1)
        
        for _Obj, _Elm, _LoadCase, _StepType, _StepNum, _F1, _F2, _F3, _M1, _M2, _M3 in zip(Obj, Elm, LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3):
            loads.append(
                {
                    'ObjectName': _Obj,
                    'ElementName': _Elm,
                    'LoadCase': _LoadCase,
                    'StepType': _StepType,
                    'StepNum': _StepNum,
                    'F1': _F1,
                    'F2': _F2,
                    'F3': _F3,
                    'M1': _M1,
                    'M2': _M2,
                    'M3': _M3
                }
            )
            
        return *loads, ret # type: ignore