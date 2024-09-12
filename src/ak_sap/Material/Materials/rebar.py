from ak_sap.utils import MasterClass, log
from ak_sap.utils.decorators import smooth_sap_do


class Rebar(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        self.PropRebar = mySapObject.SapModel.PropRebar

    @smooth_sap_do
    def rename(self, old: str, new: str):
        """changes the name of an existing rebar property."""
        return self.PropRebar.ChangeName(old, new)

    @smooth_sap_do
    def total(self) -> int:
        """returns the total number of defined rebar properties in the model."""
        return self.PropRebar.Count()

    def __len__(self) -> int:
        """returns the total number of defined rebar properties in the model."""
        return self.total()

    @smooth_sap_do
    def delete(self, name: str):
        """deletes a specified rebar property."""
        return self.PropRebar.Delete(name)

    @smooth_sap_do
    def list_all(self) -> list[str]:
        """retrieves the names of all defined rebar properties in the model."""
        _, *result = self.PropRebar.GetNameList()
        return result

    @smooth_sap_do
    def get_prop(self, name: str) -> dict:
        result = self.PropRebar.GetProp(name)
        return {"area": result[0], "dia": result[1]}

    @smooth_sap_do
    def set_prop(self, name: str, area: float, dia: float):
        return self.PropRebar.SetProp(name, area, dia)
