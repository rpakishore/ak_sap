from ak_sap.utils import log

class Point:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
    
    def __str__(self) -> str:
        return 'Instance of `Area` Element. Holds collection of model functions'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        """returns the total number of area elements in the analysis model."""
        return self.SapModel.PointObj.Count()
    
    def add_by_coord(self, point: tuple[float, float, float], name: str='', coord_sys: str = 'Global') -> str:
        """Adds point to the model

        Args:
            point (tuple[float, float, float]): x, y, z coordinates
            name (str, optional): Custom name for point. Defaults to ''.
            coord_sys (str, optional): Name of coordinate system. Defaults to 'Global'.

        Returns:
            str: Name of point
        """
        try:
            ret = self.SapModel.PointObj.AddCartesian(*point, '', name, coord_sys)
            assert ret[-1] == 0
            return ret[0]
        except Exception as e:
            log.critical(str(e))