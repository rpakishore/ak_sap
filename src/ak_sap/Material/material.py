import typing

from ak_sap.utils import MasterClass, log
from ak_sap.utils.decorators import smooth_sap_do

from .constants import MaterialTypesStr, SymmetryTypeStr
from .Materials.rebar import Rebar

class Material(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        self.PropMaterial = mySapObject.SapModel.PropMaterial
        
        #Submodules
        self.Rebar = Rebar(mySapObject=mySapObject)
    
    def __len__(self) -> int:
        return self.total()
    
    @smooth_sap_do
    def rename(self, old: str, new: str):
        """changes the name of an existing material property."""
        return self.PropMaterial.ChangeName(old, new)
    
    @smooth_sap_do
    def total(self) -> int:
        """returns the total number of defined material properties in the model."""
        return self.PropMaterial.Count()
    
    @smooth_sap_do
    def delete(self, name: str):
        return self.PropMaterial.Delete(name)
    
    @smooth_sap_do
    def list_all(self) -> list[str]:
        """retrieves the names of all defined material properties of the specified type"""
        return self.PropMaterial.GetNameList()[1:]
    
    def __get_type(self, name: str) -> dict:
        *_result, _ret = self.PropMaterial.GetTypeOAPI(name)
        assert _ret == 0
        return {
            'MaterialType': typing.get_args(MaterialTypesStr)[_result[0] - 1],
            'SymmetryType': typing.get_args(SymmetryTypeStr)[_result[1] - 1]
        }
    
    def get_props(self, name: str) -> dict:
        """retrieves some basic material property data."""
        *_result, _ret = self.PropMaterial.GetMaterial(name)
        assert _ret == 0
        return {
            'MaterialType': typing.get_args(MaterialTypesStr)[_result[0] - 1],
            'Color': _result[1],
            'Notes': _result[2],
            'GUID': _result[3],
            'SymmetryType': self.__get_type(name=name)['SymmetryType']
        }
    
    @smooth_sap_do
    def add(self, name: str, material_type: MaterialTypesStr):
        """initializes a material property. 
        If this function is called for an existing material property, all items for the material are reset to their default value."""
        return self.PropMaterial.SetMaterial(name, typing.get_args(MaterialTypesStr).index(material_type) + 1)
    
    @smooth_sap_do
    def set_isotropic(self, name: str, E: float, poisson: float, thermal_coeff: float):
        """sets the material directional symmetry type to isotropic, and assigns the isotropic mechanical properties."""
        return self.PropMaterial.SetMPIsotropic(name, E, poisson, thermal_coeff)
    
    @smooth_sap_do
    def set_density(self, name: str, mass_per_vol: float):
        """assigns weight per unit volume or mass per unit volume to a material property."""
        return self.PropMaterial.SetWeightAndMass(name, 2, mass_per_vol)
