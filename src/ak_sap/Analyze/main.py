from typing import Literal

from ak_sap.utils import MasterClass
from ak_sap.utils.decorators import smooth_sap_do


class Analyze(MasterClass):
    """Class to perform analysis operations on a SAP2000 model.

    This class encapsulates methods for creating models, running analyses,
    and retrieving analysis results.

    Attributes:
        __Analyze: The SAP2000 analyze object.
    """

    def __init__(self, mySapObject) -> None:
        """Initializes the Analyze class.

        Args:
            mySapObject: The main SAP2000 object to interface with.
        """
        super().__init__(mySapObject=mySapObject)
        self.__Analyze = mySapObject.SapModel.Analyze

    @smooth_sap_do
    def create_model(self) -> bool:
        """Creates the analysis model.

        If the analysis model already exists and is current, nothing is done.

        Returns:
            bool: True if the model was successfully created, False otherwise.
        """
        return self.__Analyze.CreateAnalyzeModel()

    @smooth_sap_do
    def run(self):
        """Runs the analysis.

        The analysis model is automatically created as part of this function.

        Returns:
            The result from the RunAnalysis function.
        """
        return self.__Analyze.RunAnalysis()

    @smooth_sap_do
    def case_status(self) -> dict:
        """Retrieves the status for all load cases.

        Returns:
            dict: A dictionary containing cases and their current status.
        """
        return case_status(ret=self.__Analyze.GetCaseStatus()), 0  # type: ignore

    @smooth_sap_do
    def get_run_flag(self) -> dict:
        """Retrieves the run flags for all analysis cases.

        Returns:
            dict: A dictionary of load cases and their run flags.
        """
        return get_run_flag(ret=self.__Analyze.GetRunCaseFlag()), 0  # type: ignore

    @smooth_sap_do
    def set_run_flag(self, case: str, status: bool):
        """Sets the run flag for load cases.

        Args:
            case (str): The name of an existing load case.
            status (bool): If True, the specified load case is to be run.
        """
        return self.__Analyze.SetRunCaseFlag(case, status)

    @smooth_sap_do
    def get_solver(self) -> dict:
        """Retrieves the model solver options.

        Returns:
            dict: A dictionary containing solver information.
        """
        return get_solver(ret=self.__Analyze.GetSolverOption_3()), 0  # type: ignore

    @smooth_sap_do
    def set_solver(
        self,
        SolverType: Literal["Standard", "Advanced", "Multi-threaded"],
        SolverProcessType: Literal["Auto", "GUI", "Separate"],
        NumberParallelRuns: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8],
        StiffCase: str = "",
    ) -> bool:
        """Sets the model solver options.

        Args:
            SolverType (Literal['Standard', 'Advanced', 'Multi-threaded']): Indicates the solver type.
            SolverProcessType (Literal['Auto', 'GUI', 'Separate']): Indicates the process the analysis is run.
            NumberParallelRuns (Literal[0-8]): Number of parallel runs.
            StiffCase (str, optional): Name of the load case used when outputting the mass and stiffness
                                         matrices to text files. Defaults to ''.

        Returns:
            bool: True if solver options were successfully set, False otherwise.
        """
        return self.__Analyze.SetSolverOption_3(
            ["Standard", "Advanced", "Multi-threaded"].index(SolverType),
            ["Auto", "GUI", "Separate"].index(SolverProcessType),
            NumberParallelRuns,
            0,
            0,
            StiffCase,
        )


def get_solver(ret: list) -> dict:
    """Parses the solver information retrieved from SAP2000.

    Args:
        ret (list): The return value from SAP2000 containing solver options.

    Returns:
        dict: A dictionary of solver information.

    Raises:
        AssertionError: If the return status indicates an error.
    """
    assert ret[-1] == 0
    return {
        "SolverType": ["Standard", "Advanced", "Multi-threaded"][ret[0]],
        "SolverProcessType": ["Auto", "GUI", "Separate"][ret[1]],
        "NumberParallelRuns": abs(ret[2]),
        "StiffCase": ret[5],
    }


def get_run_flag(ret: list) -> dict:
    """Parses the run flags retrieved from SAP2000.

    Args:
        ret (list): The return value from SAP2000 containing run flags.

    Returns:
        dict: A dictionary of load cases and their run flags.

    Raises:
        AssertionError: If the return status indicates an error.
    """
    assert ret[-1] == 0
    status: dict = {}

    if ret[0] == 1:
        # If cases is not a iterable
        return {ret[1]: ret[2]}

    # Else if cases are iterables
    for _case, _status in zip(list(ret[1]), list(ret[2])):
        status[_case] = _status
    return status


def case_status(ret: list) -> dict:
    """Parses the case status retrieved from SAP2000.

    Args:
        ret (list): The return value from SAP2000 containing case status.

    Returns:
        dict: A dictionary of cases and their statuses.

    Raises:
        AssertionError: If the return status indicates an error.
    """
    assert ret[-1] == 0
    status: dict = {}
    _status_exp = ["Not run", "Could not start", "Not finished", "Finished"]
    if ret[0] == 1:
        # If cases is not a iterable
        return {ret[1]: _status_exp[ret[2] - 1]}

    # Else if cases are iterables
    for _case, _status in zip(list(ret[1]), list(ret[2])):
        status[_case] = _status_exp[_status - 1]
    return status
