from typing import Any, Generator

from ak_sap.utils.decorators import smooth_sap_do
from ak_sap.utils.logger import log


class MasterObj:
    def __init__(self, mySapObject, ElemObj) -> None:
        self.__mySapObject = mySapObject
        self.__SapModel = mySapObject.SapModel
        self.__ElemObj = ElemObj
        print(f"`{self.__class__.__name__}` instance initialized.")

    def __str__(self) -> str:
        return f"`{self.__class__.__name__}` Instance"

    def __repr__(self) -> str:
        return self.__str__()

    def __del__(self) -> None:
        try:
            self.__mySapObject = None
            self.__SapModel = None
        except Exception as e:
            log.warning(
                msg=f"Exception faced when deleting {self.__class__.__name__}\n{e}"
            )

    def __len__(self) -> int:
        """returns the total number of point elements in the analysis model."""
        return self.__ElemObj.Count()

    def selected(self) -> Generator[str, Any, None]:
        """Returns the names of selected element objects"""
        for elem in self.all():
            if _sel := self.is_selected(name=elem):
                print(f"{elem=}, {_sel=}")
                yield elem

    def is_selected(self, name: str) -> bool:
        self.check_obj_legal(name)
        return self.__ElemObj.GetSelected(name)[0]

    @smooth_sap_do
    def all(self) -> tuple[str]:
        """Returns namelist of all element objects"""
        _, *elem_list = self.__ElemObj.GetNameList()
        return elem_list  # type: ignore

    @smooth_sap_do
    def rename(self, old_name: str, new_name: str):
        """Change the name of the element"""
        self.check_obj_legal(name=old_name)
        return self.__ElemObj.ChangeName(old_name, new_name)

    def check_obj_legal(self, name: str):
        """Confirms specified element exists in the model"""
        assert name in self.all(), (
            f"`{name}` not found in the current list of elements: {self.all()}"
        )

    @smooth_sap_do
    def delete(self, name: str):
        """Delete element from model"""
        return self.__ElemObj.Delete(name)
