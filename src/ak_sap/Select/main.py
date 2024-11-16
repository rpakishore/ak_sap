from typing import Literal

from ak_sap.utils import MasterClass, log
from ak_sap.utils.decorators import smooth_sap_do


class Select(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        self.__SelectObj = mySapObject.SapModel.SelectObj

    @smooth_sap_do
    def all(self) -> bool:
        """selects all objects in the model"""
        return self.__SelectObj.All(False)

    @smooth_sap_do
    def clear(self) -> bool:
        """Deselects all objects in model"""
        return self.__SelectObj.ClearSelection()

    @smooth_sap_do
    def constraint(self, name: str, reverse: bool = False) -> bool:
        """selects or deselects all point objects to which the specified constraint has been assigned

        Args:
            name (str): name of an existing joint constraint
            reverse (bool): deselect
        """
        return self.__SelectObj.Constraint(name, reverse)

    @property
    def selected(self) -> list[dict]:
        return selected_parse(ret=self.__SelectObj.GetSelected()), 0  # type: ignore

    @smooth_sap_do
    def in_plane(
        self, pointname: str, plane: Literal["XY", "YZ", "XZ"], reverse: bool = False
    ) -> bool:
        """selects or deselects all objects that are in the same plane as specified point object

        Args:
            pointname (str): point name
            plane (Literal['XY', 'YZ', 'XZ']): plane to select
            reverse (bool, optional): deselect. Defaults to False.

        Raises:
            Exception: If invalid plane option chosen
        """
        match plane.casefold():
            case "xy":
                return self.__SelectObj.PlaneXY(pointname, reverse)
            case "yz":
                return self.__SelectObj.PlaneYZ(pointname, reverse)
            case "xz":
                return self.__SelectObj.PlaneXZ(pointname, reverse)
            case _:
                raise Exception(f"{plane=} is not a valid choice.")

    @smooth_sap_do
    def invert(self) -> bool:
        """deselects all selected objects and selects all unselected objects"""
        return self.__SelectObj.InvertSelection()

    @smooth_sap_do
    def previous(self) -> bool:
        """restores the previous selection"""
        return self.__SelectObj.PreviousSelection()

    @smooth_sap_do
    def property(
        self,
        type: Literal["Area", "Cable", "Frame", "Link", "Material", "Solid", "Tendon"],
        name: str,
        reverse: bool = False,
    ):
        """selects or deselects all objects to which the specified property has been assigned

        Args:
            type (Literal['Area', 'Cable', 'Frame', 'Link', 'Material', 'Solid', 'Tendon']): Property Type
            name (str): Propertyname
            reverse (bool, optional): Deselect. Defaults to False.

        Raises:
            Exception: If invalid type option chosen
        """
        match type.casefold():
            case "area":
                return self.__SelectObj.PropertyArea(
                    name,
                )
            case "cable":
                return self.__SelectObj.PropertyCable(name)
            case "frame":
                return self.__SelectObj.PropertyFrame(name)
            case "link":
                return self.__SelectObj.PropertyLink(name)
            case "material":
                return self.__SelectObj.PropertyMaterial(name)
            case "solid":
                return self.__SelectObj.PropertySolid(name)
            case "tendon":
                return self.__SelectObj.PropertyTendon(name)
            case _:
                raise Exception(f"{type=} is not a valid choice.")


def selected_parse(ret: list) -> list[dict]:
    assert ret[-1] == 0
    selected: list[dict] = []

    for idx in range(ret[0]):
        selected.append(
            {
                "ObjectType": [
                    "Point",
                    "Frame",
                    "Cable",
                    "Tendon",
                    "Area",
                    "Solid",
                    "Link",
                ][ret[1][idx] - 1],
                "ObjectName": ret[2][idx],
            }
        )
    return selected
