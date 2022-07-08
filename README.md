# StrawDB
*This project is under progress* <br>
A very simple Data Server that supports CRUD command

### Table File structure

#### Type pointers
- int = 1
- float = 2
- bool = 3
- str = 4

#### Sizes (bytes)
- int = 4 
- float = 4
- bool = 1
- str = 140
- pointer = 4

#### Metadata
The starting of the file contains metadata (all integers) <br>
`[NUMBER_COLS, TYPE_COL_1, TYPE_COL_2, ... , TYPE_COL_3, LIMIT, ENTRIES_IN_LAST_TABLE]`

Following the metadata is the data <br>
_Commas and newline are for reference only_ <br>
```
COL1, POINTER, COL2, POINTER , ... , COLN, POINTER, 
COL1, POINTER, COL2, POINTER , ... , COLN, POINTER, 
                    .
                    .
                    .
                    .
                    .
COL1, POINTER, COL2, POINTER , ... , COLN, POINTER, 
```


### Query Format
```
load `table_name`
  get row 12              // Maybe can add get col?
  get row 12..18
  find `column` = `element` and `column2` = `element2` ... 
end
```

### Keywords
- **load: ** Loads the table for queries
- **end: ** Clears the cache for the loaded table
- **get: ** Get's the entire row or list of rows
- **row: ** specifier to the get command
- **find: ** finds rows that matches the query

#### ToDo
- [ ] col command _(to get a column or list of columns)_
- [ ] as command _(to store the output of query as varaible)_

