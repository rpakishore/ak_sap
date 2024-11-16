from dataclasses import dataclass


@dataclass
class ConcreteProp:
    name: str
    fc: float
    isLightweight: bool = False
    shear_reduction_factor: float = 0
