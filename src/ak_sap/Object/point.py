from ak_sap.utils import log
from ak_sap.utils.decorators import smooth_sap_do
from .helper import MasterElem

class Point(MasterElem):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject, ElemObj=mySapObject.SapModel.PointObj)
    
    @smooth_sap_do
    def add_by_coord(self, point: tuple[float, float, float], name: str='', coord_sys: str = 'Global') -> str:
        """Adds point to the model
        Args:
            point (tuple[float, float, float]): x, y, z coordinates
            name (str, optional): Custom name for point. Defaults to ''.
            coord_sys (str, optional): Name of coordinate system. Defaults to 'Global'.
        """
        return self.ElemObj.AddCartesian(*point, '', name, coord_sys)
