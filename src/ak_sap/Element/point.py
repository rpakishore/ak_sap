from ak_sap.utils import log
from ak_sap.utils.decorators import smooth_sap_do
from ak_sap.utils import MasterClass

class Point(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        self.PointObj = self.SapModel.PointObj
    
    def __str__(self) -> str:
        return 'Instance of `Point` Element. Holds collection of model functions'
    
    def __len__(self) -> int:
        """returns the total number of point elements in the analysis model."""
        return self.PointObj.Count()
    
    @smooth_sap_do
    def add_by_coord(self, point: tuple[float, float, float], name: str='', coord_sys: str = 'Global') -> str:
        """Adds point to the model

        Args:
            point (tuple[float, float, float]): x, y, z coordinates
            name (str, optional): Custom name for point. Defaults to ''.
            coord_sys (str, optional): Name of coordinate system. Defaults to 'Global'.

        Returns:
            str: Name of point
        """
        return self.PointObj.AddCartesian(*point, '', name, coord_sys)

            
    def rename(self, current: str, new: str) -> str:
        """Change name of point"""
        try:
            assert self.PointObj.ChangeName(current, new) == 0
            return new
        except Exception as e:
            log.critical(str(e))
            return current