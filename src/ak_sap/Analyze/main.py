from typing import Literal

from ak_sap.utils import MasterClass, log
from ak_sap.utils.decorators import smooth_sap_do

class Analyze(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        self.__Analyze = mySapObject.SapModel.Analyze
    
    @smooth_sap_do
    def create_model(self) -> bool:
        """creates the analysis model. 
        If the analysis model is already created and current, nothing is done.
        """
        return self.__Analyze.CreateAnalyzeModel()
    
    @smooth_sap_do
    def run(self):
        """runs the analysis. 
        The analysis model is automatically created as part of this function.
        """
        return self.__Analyze.RunAnalysis()
    
    @smooth_sap_do
    def case_status(self) -> dict:
        """retrieves the status for all load cases.

        Returns:
            list[dict]: Cases and their current status.
        """
        return case_status(ret=self.__Analyze.GetCaseStatus()), 0 # type: ignore

    @smooth_sap_do
    def get_run_flag(self) -> dict:
        """retrieves the run flags for all analysis cases.

        Returns:
            dict: Loadcases and their run flags
        """
        return get_run_flag(ret=self.__Analyze.GetRunCaseFlag()), 0 # type: ignore

    @smooth_sap_do
    def set_run_flag(self, case: str, status: bool):
        """sets the run flag for load cases

        Args:
            case (str): name of an existing load case
            status (bool): If this item is True, the specified load case is to be run
        """
        return self.__Analyze.SetRunCaseFlag(case, status)
    
    @smooth_sap_do
    def get_solver(self) -> dict:
        """retrieves the model solver options

        Returns:
            dict: Solver Info
        """
        return get_solver(ret = self.__Analyze.GetSolverOption_3()), 0 # type: ignore
    
    @smooth_sap_do
    def set_solver(self, 
                    SolverType: Literal['Standard', 'Advanced', 'Multi-threaded'],
                    SolverProcessType: Literal['Auto', 'GUI', 'Separate'],
                    NumberParallelRuns: Literal[0,1,2,3,4,5,6,7,8],
                    StiffCase: str = ''
                    ) -> bool:
        """sets the model solver options

        Args:
            SolverType (Literal['Standard', 'Advanced', 'Multi-threaded']): indicats the solver type.
            SolverProcessType (Literal['Auto', 'GUI', 'Separate']): indicats the process the analysis is run
            NumberParallelRuns (Literal[0,1,2,3,4,5,6,7,8]): Number of parallel runs
            StiffCase (str, optional): name of the load case used when outputting the mass and stiffness matrices to text files. Defaults to ''.
        """
        return self.__Analyze.SetSolverOption_3(
            ['Standard', 'Advanced', 'Multi-threaded'].index(SolverType),
            ['Auto', 'GUI', 'Separate'].index(SolverProcessType),
            NumberParallelRuns,
            0,0,
            StiffCase
        )

def get_solver(ret: list) -> dict:
    assert ret[-1] == 0
    return {
        'SolverType': ['Standard', 'Advanced', 'Multi-threaded'][ret[0]],
        'SolverProcessType': ['Auto', 'GUI', 'Separate'][ret[1]],
        'NumberParallelRuns': abs(ret[2]),
        'StiffCase': ret[5]
    }

def get_run_flag(ret: list)->dict:
    assert ret[-1] == 0
    status: dict = {}
    
    if ret[0] == 1:
        #If cases is not a iterable
        return {ret[1]: ret[2]}
    
    #Else if cases are iterables
    for _case, _status in zip(list(ret[1]), list(ret[2])):
        status[_case] =  _status
    return status

def case_status(ret: list)->dict:
    assert ret[-1] == 0
    status: dict = {}
    _status_exp = [
        'Not run',
        'Could not start',
        'Not finished',
        'Finished'
    ]
    if ret[0] == 1:
        #If cases is not a iterable
        return {ret[1]: _status_exp[ret[2]-1]}
    
    #Else if cases are iterables
    for _case, _status in zip(list(ret[1]), list(ret[2])):
        status[_case] =  _status_exp[_status-1]
    return status