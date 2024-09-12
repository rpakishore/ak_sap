from typing import Literal

from ak_sap.misc import Coord
from ak_sap.utils.decorators import smooth_sap_do

from .frame import Frame
from .point import Point


class Object:
    def __init__(self, mySapObject) -> None:
        self.__mySapObject = mySapObject
        self.__EditGeneral = mySapObject.SapModel.EditGeneral
        self.Point = Point(mySapObject=mySapObject)
        self.Frame = Frame(mySapObject=mySapObject)

    @smooth_sap_do
    def move_selected(self, dx: float, dy: float, dz: float) -> bool:
        """moves selected point, frame, cable, tendon, area, solid and link objects.

        Args:
            dx (float): x offsets
            dy (float): y offsets
            dz (float): z offsets
        """
        return self.__EditGeneral.Move(dx, dy, dz)

    @smooth_sap_do
    def copy(self, dx: float, dy: float, dz: float, num: int) -> tuple:
        """linearly replicates selected objects.

        Args:
            dx (float): x offset
            dy (float): y offset
            dz (float): z offset
            num (int): number of times the selected objects are to be replicated.
        """
        return self.__EditGeneral.ReplicateLinear(dx, dy, dz, num)

    @smooth_sap_do
    def mirror(self, plane: Literal["X", "Y", "Z"], coord1: Coord, coord2: Coord):
        """mirror replicates selected objects

        Args:
            plane (Literal['X', 'Y', 'Z']): parallel to this plane
            coord1 (Coord), coord2 (Coord): define the intersection of the mirror plane with the perp. plane
        """
        axis = ["Z", "X", "Y"].index(plane.upper().strip()) + 1
        return self.__EditGeneral.ReplicateMirror(
            axis, *coord1.as_tuple(), *coord2.as_tuple()
        )
