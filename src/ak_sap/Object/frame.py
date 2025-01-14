from ak_sap.utils.decorators import smooth_sap_do

from .helper import MasterObj


class Frame(MasterObj):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject, ElemObj=mySapObject.SapModel.FrameObj)

        self.__EditFrame = mySapObject.SapModel.EditFrame
        self.__EditGeneral = mySapObject.SapModel.EditGeneral
        self.__FrameObj = mySapObject.SapModel.FrameObj

        self.Prop = Prop(mySapObject=mySapObject)

    @smooth_sap_do
    def get_section(self, name: str) -> str:
        self.check_obj_legal(name=name)
        _ret = self.__FrameObj.GetSection(name)
        return (_ret[0], _ret[-1])  # type: ignore

    @smooth_sap_do
    def get_points(self, name: str) -> tuple[str]:
        """retrieves the names of the point objects at each end of a specified frame object."""
        # self.check_obj_legal(name=name)
        return self.__FrameObj.GetPoints(name)

    @smooth_sap_do
    def divide_by_distance(
        self, name: str, dist: float, Iend: bool = True
    ) -> tuple[str]:
        """divides straight frame objects into two objects at a location defined by the Dist and IEnd items.
        Curved frame objects are not divided.
        """
        return self.__EditFrame.DivideAtDistance(name, dist, Iend)

    @smooth_sap_do
    def divide_by_intersection(self, name: str) -> tuple[str]:
        """divides straight frame objects at intersections with selected point objects, line objects, area edges and solid edges.
        Curved frame objects are not divided.

        Args:
            name (str): Frame Name

        Returns:
            tuple[str]: array that includes the names of the new frame objects.
        """
        return self.__EditFrame.DivideAtIntersections(name)[1:]

    @smooth_sap_do
    def divide_by_ratio(
        self, name: str, ratio: float, num_frames: int = 1
    ) -> tuple[str]:
        """divides straight frame objects based on a specified Last/First length ratio.
        Curved frame objects are not divided.

        Args:
            name (str): name of an existing straight frame object.
            ratio (float): Last/First length ratio for the new frame objects.
            num_frames (int, optional): frame object is divided into this number of new objects. Defaults to 1.

        Returns:
            tuple[str]: array that includes the names of the new frame objects.
        """
        return self.__EditFrame.DivideByRatio(name, num_frames, ratio)

    @smooth_sap_do
    def join(self, frame1: str, frame2: str) -> bool:
        """joins two straight frame objects that have a common end point and are colinear.

        Args:
            frame1 (str): name of an existing frame object to be joined. The new, joined frame object keeps this name.
            frame2 (_type_): name of an existing frame object to be joined.
        """
        return self.__EditFrame.Join(frame1, frame2)

    @smooth_sap_do
    def change_points(self, name: str, point1: str, point2: str) -> bool:
        """modifies the connectivity of a frame object.

        Args:
            name (str): name of an existing frame object
            point1 (str): name of the point object at the I-End of the frame object.
            point2 (str): name of the point object at the J-End of the frame object.
        """
        return self.__EditFrame.ChangeConnectivity(name, point1, point2)

    @smooth_sap_do
    def extrude(
        self,
        frame_name: str,
        dx: float,
        dy: float,
        dz: float,
        num_areas: int,
        property_name: str | None = None,
        del_frame: bool = False,
    ) -> list[str]:
        """Creates new area objects by linearly extruding a specified frame obj.

        Args:
            frame_name (str): Name of existing frame to extrude
            dx (float): x offset.
            dy (float): y offset.
            dz (float): z offset.
            num_areas (int): number of area objects to create
            property_name (str | None, optional): Name of a defined area section property to be used for the new obj. Defaults to None.
            del_frame(bool, optional): If this item is True, the straight frame object indicated by the Name item is deleted after the extrusion is complete. Defaults to False.

        Returns:
            list[str]: array of the name of each area object created
        """
        return self.__EditGeneral.ExtrudeFrameToAreaLinear(
            frame_name, property_name, dx, dy, dz, num_areas, del_frame
        )


class Prop:
    def __init__(self, mySapObject) -> None:
        self.__mySapObject = mySapObject.SapModel

    def __len__(self) -> int:
        return self.total()

    @smooth_sap_do
    def rename(self, old_name: str, new_name: str):
        """changes the name of an existing frame section property."""
        return self.__mySapObject.PropFrame.ChangeName(old_name, new_name)

    @smooth_sap_do
    def total(self) -> int:
        """returns the total number of defined frame section properties in the model"""
        return self.__mySapObject.PropFrame.Count()
