from typing import Literal

import pandas as pd

from ak_sap.utils.decorators import smooth_sap_do

from .helper import MasterObj


class Point(MasterObj):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject, ElemObj=mySapObject.SapModel.PointObj)
        self.__EditPoint = mySapObject.SapModel.EditPoint
        self.__PointObj = mySapObject.SapModel.PointObj
        self.__EditGeneral = mySapObject.SapModel.EditGeneral

    @smooth_sap_do
    def add_by_coord(
        self,
        point: tuple[float, float, float],
        name: str = "",
        coord_sys: Literal["Local", "GLOBAL"] = "GLOBAL",
    ) -> str:
        """Adds point to the model
        Args:
            point (tuple[float, float, float]): x, y, z coordinates
            name (str, optional): Custom name for point. Defaults to ''.
            coord_sys (str, optional): Name of coordinate system. Defaults to 'GLOBAL'.
        """
        return self.__PointObj.AddCartesian(*point, "", name, coord_sys)

    @smooth_sap_do
    def align(self, axis: Literal["X", "Y", "Z"], ordinate: float) -> tuple:
        """aligns selected point objects.

        Args:
            axis (Literal['X', 'Y', 'Z']): Align points to this ordinate in present coordinate system
            ordinate (float): The X, Y or Z ordinate that applies

        Returns:
            tuple: (number of point objects that are in a new location after the alignment is complete.,
            array of the name of each point object that is in a new location after the alignment is complete.)
        """
        _axis = ["X", "Y", "Z"].index(axis.upper().strip()) + 1
        return self.__EditPoint.Align(_axis, ordinate)

    @smooth_sap_do
    def select(self, name: str) -> bool:
        return self.__PointObj.SetSelected(name, True)

    @smooth_sap_do
    def deselect(self, name: str) -> bool:
        return self.__PointObj.SetSelected(name, False)

    @smooth_sap_do
    def deselect_all(self) -> bool:
        return self.__PointObj.ClearSelection()

    @smooth_sap_do
    def merge(self, tolerance: float) -> tuple:
        """merges selected point objects that are within a specified distance of one another.

        Args:
            tolerance (float): Point objects within this distance of one another are merged into one point object.

        Returns:
            tuple: (number of the selected point objects that still exist after the merge is complete.,
            array of the name of each selected point object that still exists after the merge is complete.)
        """
        return self.__EditPoint.Merge(tolerance)

    @smooth_sap_do
    def change_coord(self, name: str, x: float, y: float, z: float) -> bool:
        """changes the coordinates of a specified point object.

        Args:
            name (str): name of an existing point object.
            x (float): new x coordinate.
            y (float): new y coordinate.
            z (float): new z coordinate.

        Returns:
            bool: Success
        """
        return self.__EditPoint.ChangeCoordinates_1(name, x, y, z)

    @smooth_sap_do
    def extrude(
        self,
        point_name: str,
        dx: float,
        dy: float,
        dz: float,
        num_frames: int,
        property_name: str | None = None,
    ) -> list[str]:
        """Creates new frame objects by linearly extruding a specified point obj. into frame objects.

        Args:
            point_name (str): Name of existing point to extrude
            dx (float): x offset.
            dy (float): y offset.
            dz (float): z offset.
            num_frames (int): number of frame objects to create
            property_name (str | None, optional): Name of a defined frame section property to be used for the new frame obj. Defaults to None.

        Returns:
            list[str]: array of the name of each frame object created
        """
        return self.__EditGeneral.ExtrudePointToFrameLinear(
            point_name, property_name, dx, dy, dz, num_frames
        )

    @smooth_sap_do
    def setLoadForce(
        self,
        name: str,
        loadpattern: str,
        f1: float = 0,
        f2: float = 0,
        f3: float = 0,
        m1: float = 0,
        m2: float = 0,
        m3: float = 0,
        replace: bool = True,
        coord_sys: Literal["Local", "GLOBAL"] = "Local",
    ):
        """makes point load assignments to point objects."""
        return self.__PointObj.SetLoadForce(
            name, loadpattern, [f1, f2, f3, m1, m2, m3], replace, coord_sys
        )

    @smooth_sap_do
    def setLoadDisplacement(
        self,
        name: str,
        loadpattern: str,
        u1: float = 0,
        u2: float = 0,
        u3: float = 0,
        r1: float = 0,
        r2: float = 0,
        r3: float = 0,
        replace: bool = True,
        coord_sys: Literal["Local", "GLOBAL"] = "Local",
    ):
        """makes ground displacement load assignments to point objects."""
        return self.__PointObj.SetLoadDispl(
            name, loadpattern, [u1, u2, u3, r1, r2, r3], replace, coord_sys
        )

    @smooth_sap_do
    def getLoadForce(self, name: str) -> pd.DataFrame:
        """retrieves the joint force load assignments to point objects."""
        ret = self.__PointObj.GetLoadForce(name)[1:]
        data = {
            "PointName": ret[0],
            "LoadPattern": ret[1],
            "CSys": ret[3],
            "F1": ret[4],
            "F2": ret[5],
            "F3": ret[6],
            "M1": ret[7],
            "M2": ret[8],
            "M3": ret[9],
        }

        return pd.DataFrame(data)

    @smooth_sap_do
    def getLoadDisplacement(self, name: str) -> pd.DataFrame:
        """retrieves the ground displacement load assignments to point objects."""
        ret = self.__PointObj.GetLoadDispl(name)[1:]
        data = {
            "PointName": ret[0],
            "LoadPattern": ret[1],
            "CSys": ret[3],
            "U1": ret[4],
            "U2": ret[5],
            "U3": ret[6],
            "R1": ret[7],
            "R2": ret[8],
            "R3": ret[9],
        }

        return pd.DataFrame(data)

    @smooth_sap_do
    def delLoadDisplacement(self, name: str, loadpattern: str) -> bool:
        """deletes all ground displacement load assignments, for the specified load pattern, from the specified point object(s)."""
        return self.__PointObj.DeleteLoadDispl(name, loadpattern)

    @smooth_sap_do
    def delLoadForce(self, name: str, loadpattern: str) -> bool:
        """deletes all point load assignments, for the specified load pattern, from the specified point object(s)."""
        return self.__PointObj.DeleteLoadForce(name, loadpattern)

    @smooth_sap_do
    def changename(self, name: str, new_name: str) -> bool:
        """returns zero if the new name is successfully applied, otherwise it returns a nonzero value.

        Args:
            name (str): existing name of a point object.
            new_name (str): new name for the point object.

        Returns:
            bool: returns zero if the new name is successfully applied, otherwise it returns a nonzero value.
        """
        return self.__PointObj.ChangeName(name, new_name)

    def __len__(self) -> int:
        """returns the total number of point objects in the model."""
        return self.__PointObj.Count()

    @smooth_sap_do
    def delConstraint(self, name: str):
        """deletes all constraint assignments from the specified point object(s)."""
        return self.__PointObj.DeleteConstraint(name)

    @smooth_sap_do
    def setConstraint(self, name: str, constraintname: str):
        """makes joint constraint assignments to point objects"""
        return self.__PointObj.SetConstraint(name, constraintname)

    @smooth_sap_do
    def delRestraint(self, name: str):
        """deletes all restraint assignments from the specified point object"""
        return self.__PointObj.DeleteRestraint(name)

    @smooth_sap_do
    def getRestraint(self, name: str) -> pd.DataFrame:
        U1, U2, U3, R1, R2, R3 = self._PointObj.GetRestraint(name)[0]

        return pd.DataFrame(
            {
                "Point": [name],
                "U1": U1,
                "U2": U2,
                "U3": U3,
                "R1": R1,
                "R2": R2,
                "R3": R3,
            }
        )

    @smooth_sap_do
    def setRestraint(
        self, name: str, U1: bool, U2: bool, U3: bool, R1: bool, R2: bool, R3: bool
    ):
        """assigns the restraint assignments for a point object.
        The restraint assignments are always set in the point local coordinate system.
        """
        return self._PointObj.SetRestraint(name, [U1, U2, U3, R1, R2, R3])

    @smooth_sap_do
    def delSpring(self, name: str):
        """deletes all point spring assignments from the specified point object

        Args:
            name (str): name of a point object or a group depending on the value selected for ItemType item
        """
        return self.__PointObj.DeleteSpring(name)

    @smooth_sap_do
    def setSpring(
        self,
        name: str,
        U1: float,
        U2: float,
        U3: float,
        R1: float,
        R2: float,
        R3: float,
        coord_sys: Literal["Local", "GLOBAL"] = "Local",
        replace: bool = True,
    ):
        """assigns coupled springs to a point object

        Args:
            name (str): name of an existing point object or group depending on the value of the ItemType item
            U1 (float): Spring Constant for U1
            U2 (float): Spring Constant for U2
            U3 (float): Spring Constant for U3
            R1 (float): Spring Constant for R1
            R2 (float): Spring Constant for R2
            R3 (float): Spring Constant for R3
            coord_sys (Literal["Local", "GLOBAL"], optional): Coordinate System. Defaults to "Local".
            replace (bool, optional): replace existing assignment. Defaults to True.
        """
        return self.__PointObj.SetSpring(
            name, [U1, U2, U3, R1, R2, R3], 0, coord_sys == "Local", replace
        )
