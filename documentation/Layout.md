- [1. Layout](#1-layout)
  - [1.1. Roadmap/Checklist](#11-roadmapchecklist)
  - [1.2. Sub-Modules](#12-sub-modules)
    - [1.2.1. Model](#121-model)
    - [1.2.2. Element](#122-element)
    - [1.2.3. Table](#123-table)
    - [1.2.4. Loads](#124-loads)
      - [1.2.4.1. Load Patterns](#1241-load-patterns)

# 1. Layout

## 1.1. Roadmap/Checklist

![MindMap](assets/mindmap.png)

## 1.2. Sub-Modules

### 1.2.1. Model

Collection of methods and attributes that control changes to the model as a whole

Usage Examples

```python
#Model
sap.Model.units                             #Returns current model units
sap.Model.units_database                    #Returns Internal Database units
sap.Model.set_units(value='N_m_C')          #Changes the present units of model

sap.Model.merge_tol                         #retrieves the value of the program auto merge tolerance
sap.Model.set_merge_tol(0.05)               #sets the program auto merge tolerance

sap.Model.filepath                          #Returns filepath of current file

sap.Model.is_locked                         #Returns if the model is locked
sap.Model.lock()                            #Locks the model
sap.Model.unlock()                          #Unlocks the model

sap.Model.project_info                      #Returns a dict of Project Info
##Set project info, use `.project_info` to see available keys
sap.Model.set_project_info({'Design Code': 'BCBC 2018'})

sap.Model.logs                              #Retrieve user comments and logs
sap.Model.set_logs('Add this comment')      #Adds user comments/logs
```

### 1.2.2. Element

Collection of methods and attributes that apply changes to elements in the model

Usage Examples

```python
##Points
len(sap.Element.Point)                      #list number of points in model
sap.Element.Point.add_by_coord((1,2,3))     #Add point to model
```

### 1.2.3. Table

Control the database values

Usage Examples

```python
#Database
sap.Table.list_available()                            #Lists available database tables
sap.Table.list_all()                        #Lists all database tables
```

### 1.2.4. Loads

Control the definition and assignments of loads.

#### 1.2.4.1. Load Patterns

Usage Examples

```python
pattern = sap.Load.Pattern
len(pattern)                   # List the number of load patterns defined
pattern.list()                 #List defined load patterns
pattern.rename('Dead', 'Live') #Rename previously defined pattern
pattern.delete(name='Dead')    #Delete a load pattern

pattern.get_selfwt_multiplier('DEAD')           #Get defined self weight multiplier
pattern.set_selfwt_multiplier('DEAD', 1.15)     #Set self weight multiplier

pattern.get_loadtype('DEAD')                        #Get the defined load type
pattern.set_loadtype('DEAD', pattern_type='LIVE')   #Set the defined load type

#Add a Live load case with name "Custom Live", a 1.15x self weight multiplier and also generate an accompanying load case
pattern.add(name='Custom Live', pattern_type='LIVE', 
            selfwt_multiplier=1.15, add_case=True)
```
