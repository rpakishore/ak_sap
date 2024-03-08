from .point import Point
from .frame import Frame
from ak_sap.utils.decorators import smooth_sap_do

class Object:
    def __init__(self, mySapObject) -> None:
        self.__mySapObject = mySapObject
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
        self.__mySapObject.SapModel.EditGeneral.Move(dx, dy, dz)