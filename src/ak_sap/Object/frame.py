from ak_sap.utils import log
from ak_sap.utils.decorators import smooth_sap_do
from .helper import MasterElem

class Frame(MasterElem):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject, ElemObj=mySapObject.SapModel.FrameObj)
    
    @smooth_sap_do
    def get_section(self, frame_name: str) -> str:
        self.check_element_legal(name=frame_name)
        _ret = self.ElemObj.GetSection(frame_name)
        return (_ret[0], _ret[-1]) # type: ignore
    
    @smooth_sap_do
    def get_points(self, frame_name: str) -> tuple[str]:
        """retrieves the names of the point objects at each end of a specified frame object."""
        #self.check_element_legal(name=frame_name)
        return self.ElemObj.GetPoints(frame_name)
    