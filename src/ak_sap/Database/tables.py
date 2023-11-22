import pandas as pd

import typing

from ak_sap.utils import log
from .table_data import DatabaseTable, ImportType_Literals, FieldData

class Table:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
        log.debug('Instance of `Table` module initialized.')

    def __str__(self) -> str:
        return 'Instance of Database `Table`. Holds collection of model functions'

    def list_all(self) -> list[DatabaseTable]:
        """Returns all of the tables along with their import type and 
        indicates if any data is available in the model to fill the table."""
        log.debug('Getting a list of all Tables')
        _table_data = self.SapModel.DatabaseTables.GetAllTables()
        tables = []
        for _TableKey, _TableName, _ImportType, _IsEmpty in zip(*_table_data[1:-1]):
            _import = typing.get_args(ImportType_Literals)[_ImportType]
            tables.append(DatabaseTable(
                TableKey=_TableKey, TableName=_TableName, ImportType=_import, IsEmpty=_IsEmpty))
        log.debug(f'{len(tables)} tables found')
        return tables
    
    def list_available(self) -> list[DatabaseTable]:
        """Returns all available tables along with their import type."""
        log.debug('Getting a list of all available Tables')
        _table_data = self.SapModel.DatabaseTables.GetAvailableTables()
        tables = []
        for _TableKey, _TableName, _ImportType in zip(*_table_data[1:-1]):
            _import = typing.get_args(ImportType_Literals)[_ImportType]
            tables.append(DatabaseTable(
                TableKey=_TableKey, TableName=_TableName, ImportType=_import, IsEmpty=False))
        log.debug(f'{len(tables)} tables found')
        return tables
    
    def get_table_fields(self, TableKey: str) -> list[FieldData]:
        """Returns the available fields in a specified table."""
        log.debug(f'Extracting available fields in `TableKey`: {TableKey}')
        _table_data = self.SapModel.DatabaseTables.GetAllFieldsInTable(TableKey)
        tables = []
        for _FieldKey, _FieldName, _Description, _UnitsStr, _isImportable in zip(*_table_data[2:-1]):
            tables.append(FieldData(
                FieldKey=_FieldKey, FieldName=_FieldName, Description=_Description, UnitsStr=_UnitsStr, isImportable=_isImportable
            ))
        return tables
    
    def data(self, TableKey: str) -> pd.DataFrame:
        """Extract Table Data. 
        See `.list_available()` for `TableKey`s.
        See `.get_table_fields()` for info on fields."""
        log.debug(f'Extracting data for TableKey: {TableKey}')
        _data: list = []
        try:
            _data = self.SapModel.DatabaseTables.GetTableForDisplayArray(TableKey,'','')
            assert _data[-1] == 0
            df = _array_to_pandas(headers=_data[2], array=_data[4])
            log.debug(f'Info of retrieved dataframe: \n{df.info(verbose=True)}')
            return df
        except Exception as e:
            log.critical(str(e) + f'\ndata: {_data}')
            return pd.DataFrame()
    
    def update(self, TableKey: str, data: pd.DataFrame, apply: bool=True):
        log.debug(f'Updating the values for TableKey: {TableKey}')
        TableVersion: int = 1
        self.SapModel.DatabaseTables.SetTableForEditingArray(TableKey,TableVersion,tuple(data.columns), len(data), flatten_dataframe(data))
        if apply:
            self.apply()
            
    def apply(self):
        """Instructs the program to interactively import all of the tables stored 
        in the table list using the `SetTableForEditing` functions.
        If the model is locked at the time this command is called then only tables 
        that can be interactively imported when the model is locked will be imported. 
        """
        log.debug('Applying changes to database')
        ret = []
        try:
            ret = self.SapModel.DatabaseTables.ApplyEditedTables(True)
            if ret[0] != 0 or ret[1] != 0:
                log.error(ret[-2])
            elif ret[2] != 0:
                log.warning(ret[-2])
            elif ret[3] != 0:
                log.info(ret[-2])
            else:
                log.debug(ret[-2])
            assert ret[-1] == 0
        except Exception as e:
            log.critical(str(e) + f'Return data: {ret}')
        
def _array_to_pandas(headers: tuple[str], array: tuple) -> pd.DataFrame:
    """Given the table headers as tuple and table data as a single tuple;
    Returns table as a dataframe."""
    num_fields = len(headers)
    assert len(array) % num_fields == 0, f'Array length ({len(array)}) is not divisible by header length ({num_fields})'
    
    df_data:dict[str,list] = {header: [] for header in headers}
    for array_idx, value in enumerate(array):
        _header: str = headers[array_idx % num_fields]
        df_data[_header].append(value)
    return pd.DataFrame(df_data)

def flatten_dataframe(df: pd.DataFrame) -> tuple:
    """Convert values of a dataframe to single-dimension array for SapOAPI"""
    df = df.fillna('')
    df = df.astype(str)

    flattened_list = []
    for _, row in df.iterrows():
        flattened_list.extend(row.values)
        
    modified_list = [value if value != '' else None for value in flattened_list]
    return tuple(modified_list)