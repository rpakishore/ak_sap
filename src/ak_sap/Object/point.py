from typing import Literal

from ak_sap.utils import log
from ak_sap.utils.decorators import smooth_sap_do
from .helper import MasterObj

class Point(MasterObj):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject, ElemObj=mySapObject.SapModel.PointObj)
        self.__EditPoint = mySapObject.SapModel.EditPoint
        self.__PointObj = mySapObject.SapModel.PointObj
        self.__EditGeneral = mySapObject.SapModel.EditGeneral
    
    @smooth_sap_do
    def add_by_coord(self, point: tuple[float, float, float], name: str='', coord_sys: str = 'Global') -> str:
        """Adds point to the model
        Args:
            point (tuple[float, float, float]): x, y, z coordinates
            name (str, optional): Custom name for point. Defaults to ''.
            coord_sys (str, optional): Name of coordinate system. Defaults to 'Global'.
        """
        return self.ElemObj.AddCartesian(*point, '', name, coord_sys)

    @smooth_sap_do
    def align(self, axis: Literal['X', 'Y', 'Z'], ordinate: float) -> tuple:
        """aligns selected point objects.

        Args:
            axis (Literal['X', 'Y', 'Z']): Align points to this ordinate in present coordinate system
            ordinate (float): The X, Y or Z ordinate that applies

        Returns:
            tuple: (number of point objects that are in a new location after the alignment is complete.,
            array of the name of each point object that is in a new location after the alignment is complete.)
        """
        _axis = ['X','Y','Z'].index(axis.upper().strip()) + 1
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
    def extrude(self, point_name: str, dx: float, dy: float, dz: float, num_frames: int, property_name: str|None = None) -> list[str]:
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
        return self.__EditGeneral.ExtrudePointToFrameLinear(point_name, property_name, dx, dy, dz, num_frames)