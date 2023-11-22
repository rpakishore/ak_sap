from dataclasses import dataclass
from typing import Literal

ImportType_Literals = Literal['not importable',
'importable, but not interactively importable',
'importable and interactive importable when he model is unlocked',
'importable and interactive importable when he model is unlocked and locked',]


@dataclass
class DatabaseTable:
    TableKey: str
    TableName: str
    ImportType: ImportType_Literals
    IsEmpty: bool
    
@dataclass
class FieldData:
    FieldKey: str
    FieldName: str
    Description: str
    UnitsStr: str
    isImportable: bool