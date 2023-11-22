from dataclasses import dataclass
from .table_constants import ImportType_Literals

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