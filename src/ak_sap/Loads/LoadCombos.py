from ak_sap.utils import MasterClass, log
from ak_sap.utils.decorators import smooth_sap_do


class LoadCombo(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        self.__RespCombo = mySapObject.SapModel.RespCombo

    def __str__(self) -> str:
        return "Instance of `LoadCombo`"

    @smooth_sap_do
    def list_all(self) -> tuple[str]:
        """retrieves the names of all defined response combinations"""
        return self.__RespCombo.GetNameList()[1:]
