from dataclasses import dataclass

@dataclass
class Coord:
    x: float
    y: float
    z: float
    
    def as_tuple(self) -> tuple[float]:
        return (self.x, self.y, self.z)