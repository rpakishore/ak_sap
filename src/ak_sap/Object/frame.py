from typing import Literal

from ak_sap.utils import log
from ak_sap.utils.decorators import smooth_sap_do
from .helper import MasterObj

class Frame(MasterObj):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject, ElemObj=mySapObject.SapModel.FrameObj)
        
        self.EditFrame = mySapObject.SapModel.EditFrame
        self.Prop = Prop(mySapObject=mySapObject)
    
    @smooth_sap_do
    def get_section(self, frame_name: str) -> str:
        self.check_obj_legal(name=frame_name)
        _ret = self.ElemObj.GetSection(frame_name)
        return (_ret[0], _ret[-1]) # type: ignore
    
    @smooth_sap_do
    def get_points(self, frame_name: str) -> tuple[str]:
        """retrieves the names of the point objects at each end of a specified frame object."""
        #self.check_obj_legal(name=frame_name)
        return self.ElemObj.GetPoints(frame_name)
    
    @smooth_sap_do
    def divide_by_distance(self, frame_name: str, dist: float, Iend: bool=True, num_divisions: int=1):
        return self.EditFrame.DivideAtDistance(frame_name, dist, Iend)

class Prop:
    def __init__(self, mySapObject) -> None:
        self.SapModel=mySapObject.SapModel
    
    def __len__(self) -> int:
        return self.total()
    
    @smooth_sap_do
    def rename(self, old_name: str, new_name: str):
        """changes the name of an existing frame section property."""
        return self.SapModel.PropFrame.ChangeName(old_name, new_name)
    
    @smooth_sap_do
    def total(self) -> int:
        """returns the total number of defined frame section properties in the model"""
        return self.SapModel.PropFrame.Count()