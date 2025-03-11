from dataclasses import dataclass

from .table_constants import ImportType_Literals


@dataclass
class DatabaseTable:
    """Represents a database table in SAP2000.

    Attributes:
        TableKey (str): The key identifier for the table.
        TableName (str): The name of the table.
        ImportType (ImportType_Literals): The type of importability for the table.
        IsEmpty (bool): Indicates if the table is empty.
    """

    TableKey: str
    TableName: str
    ImportType: ImportType_Literals
    IsEmpty: bool


@dataclass
class FieldData:
    """Represents a field within a database table.

    Attributes:
        FieldKey (str): The key identifier for the field.
        FieldName (str): The name of the field.
        Description (str): A brief description of the field.
        UnitsStr (str): The units associated with the field.
        isImportable (bool): Indicates if the field is importable.
    """

    FieldKey: str
    FieldName: str
    Description: str
    UnitsStr: str
    isImportable: bool
