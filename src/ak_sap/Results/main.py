from typing import Literal

from ak_sap.utils import log, MasterClass
from ak_sap.utils.decorators import smooth_sap_do
from .Setup import ResultsSetup

class Results(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        self.__Results = mySapObject.SapModel.Results
        
        self.Setup = ResultsSetup(mySapObject=mySapObject)
        
    @smooth_sap_do
    def delete(self, casename: str|Literal['All']) -> bool:
        """deletes results for load cases.

        Args:
            casename (str | Literal['All']): name of an existing load case that is to have its results deleted.
        """
        return self.mySapObject.SapModel.Analyze.DeleteResykts(casename, casename.casefold() == 'all') # type: ignore
    
    @smooth_sap_do
    def joint_reactions(self, jointname:str) -> list[dict]:
        """reports the joint reactions for the specified point elements

        Args:
            jointname (str): name of an existing point object
        """
        return joint_reactions_parse(ret=self.__Results.JointReact(jointname, 1)), 0 # type: ignore


    @smooth_sap_do
    def joint_displacements(self, jointname:str) -> list[dict]:
        """reports the joint displacements for the specified point elements

        Args:
            jointname (str): name of an existing point object
        """
        return joint_displacements_parse(ret=self.__Results.JointDispl(jointname, 1)), 0 # type: ignore
    
    @smooth_sap_do
    def joint_accelerations(self, jointname:str) ->  list[dict]:
        """reports the joint accelerations for the specified point elements

        Args:
            jointname (str): name of an existing point object
        """
        return joint_displacements_parse(ret=self.__Results.JointAcc(jointname, 1)), 0 # type: ignore
            
    @smooth_sap_do
    def joint_velocities(self, jointname:str, format: Literal['Pandas', 'List']= 'List') ->  list[dict]:
        """reports the joint velocities for the specified point elements

        Args:
            jointname (str): name of an existing point object
        """
        return joint_displacements_parse(ret=self.__Results.JointVel(jointname, 1)), 0 # type: ignore
            
def joint_displacements_parse(ret: list) -> list[dict]:
    assert ret[-1] == 0
    displacements: list[dict] = []
    
    if ret[0] == 1:
        return [
            {
                'ObjectName': ret[1],  #the point object name associated with each result, if any.
                'ElementName': ret[2], #the point element name associated with each result.
                'LoadCase': ret[3],    #name of the analysis case or load combination associated with each result.
                'StepType': ret[4],    #step type, if any, for each result.
                'StepNum': ret[5],     #includes the step number, if any, for each result.
                'U1': ret[6],          #displacement in the point element local 1 axis
                'U2': ret[7],          #displacement in the point element local 2 axis
                'U3': ret[8],          #displacement in the point element local 3 axis
                'R1': ret[9],          #rotation about the point element local 1 axis
                'R2': ret[10],         #rotation about the point element local 2 axis
                'R3': ret[11],         #rotation about the point element local 3 axis
            }
        ]
    for idx in range(ret[0]):
        displacements.append(
            {
                'ObjectName': ret[1][idx],  #the point object name associated with each result, if any.
                'ElementName': ret[2][idx], #the point element name associated with each result.
                'LoadCase': ret[3][idx],    #name of the analysis case or load combination associated with each result.
                'StepType': ret[4][idx],    #step type, if any, for each result.
                'StepNum': ret[5][idx],     #includes the step number, if any, for each result.
                'U1': ret[6][idx],          #displacement in the point element local 1 axis
                'U2': ret[7][idx],          #displacement in the point element local 2 axis
                'U3': ret[8][idx],          #displacement in the point element local 3 axis
                'R1': ret[9][idx],          #rotation about the point element local 1 axis
                'R2': ret[10][idx],         #rotation about the point element local 2 axis
                'R3': ret[11][idx],         #rotation about the point element local 3 axis
            }
        )
    return displacements

def joint_reactions_parse(ret: list) -> list[dict]:
    assert ret[-1] == 0
    loads: list[dict] = []
    
    if ret[0] == 1:
        return [
            {
                'ObjectName': ret[1],  #the point object name associated with each result, if any.
                'ElementName': ret[2], #the point element name associated with each result.
                'LoadCase': ret[3],    #name of the analysis case or load combination associated with each result.
                'StepType': ret[4],    #step type, if any, for each result.
                'StepNum': ret[5],     #includes the step number, if any, for each result.
                'F1': ret[6],          #reaction forces in the point element local 1 axis
                'F2': ret[7],          #reaction forces in the point element local 2 axis
                'F3': ret[8],          #reaction forces in the point element local 3 axis
                'M1': ret[9],          #reaction moments about the point element local 1 axis
                'M2': ret[10],         #reaction moments about the point element local 2 axis
                'M3': ret[11],         #reaction moments about the point element local 3 axis
            }
        ]
    for idx in range(ret[0]):
        loads.append(
            {
                'ObjectName': ret[1][idx],  #the point object name associated with each result, if any.
                'ElementName': ret[2][idx], #the point element name associated with each result.
                'LoadCase': ret[3][idx],    #name of the analysis case or load combination associated with each result.
                'StepType': ret[4][idx],    #step type, if any, for each result.
                'StepNum': ret[5][idx],     #includes the step number, if any, for each result.
                'F1': ret[6][idx],          #reaction forces in the point element local 1 axis
                'F2': ret[7][idx],          #reaction forces in the point element local 2 axis
                'F3': ret[8][idx],          #reaction forces in the point element local 3 axis
                'M1': ret[9][idx],          #reaction moments about the point element local 1 axis
                'M2': ret[10][idx],         ##reaction moments about the point element local 2 axis
                'M3': ret[11][idx],         ##reaction moments about the point element local 3 axis
            }
        )
    return loads