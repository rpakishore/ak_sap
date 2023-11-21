from .table_data import DatabaseTable

class Table:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel

    def __str__(self) -> str:
        return 'Instance of Database `Table`. Holds collection of model functions'

    def list_all(self) -> list[DatabaseTable]:
        """Returns all of the tables along with their import type and 
        indicates if any data is available in the model to fill the table."""
        _table_data = self.SapModel.DatabaseTables.GetAllTables()
        tables = []
        for _TableKey, _TableName, _ImportType, _IsEmpty in zip(*_table_data[1:-1]):
            match _ImportType:
                case 0:
                    _import = 'not importable'
                case 1:
                    _import = 'importable, but not interactively importable'
                case 2:
                    _import = 'importable and interactive importable when he model is unlocked'
                case 3:
                    _import = 'importable and interactive importable when he model is unlocked and locked'
                case _:
                    raise Exception(f'Unknown `ImportType`: {_ImportType}')
            tables.append(DatabaseTable(TableKey=_TableKey, TableName=_TableName, ImportType=_import, IsEmpty=_IsEmpty))
        return tables
    
    def list(self) -> list[DatabaseTable]:
        """Returns all available tables along with their import type."""
        _table_data = self.SapModel.DatabaseTables.GetAvailableTables()
        tables = []
        for _TableKey, _TableName, _ImportType in zip(*_table_data[1:-1]):
            match _ImportType:
                case 0:
                    _import = 'not importable'
                case 1:
                    _import = 'importable, but not interactively importable'
                case 2:
                    _import = 'importable and interactive importable when he model is unlocked'
                case 3:
                    _import = 'importable and interactive importable when he model is unlocked and locked'
                case _:
                    raise Exception(f'Unknown `ImportType`: {_ImportType}')
            tables.append(DatabaseTable(TableKey=_TableKey, TableName=_TableName, ImportType=_import, IsEmpty=False))
        return tables