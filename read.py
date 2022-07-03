from sys import argv
from struct import pack, unpack

# global variables
dataTypeSizes = [4, 4, 1, 140]
specifiers = ["i", "f", "?", "140s"]
# global variables

# table object
class tableObj:
    def __init__(self, table):
        self.f = open(table,'rb+')
        self.columnCount = unpack("i", self.f.read(4))[0]
        self.metaDataBytes = 4 + self.columnCount*4 + 4 + 4
        self.colTypes = unpack(f"{self.columnCount}i",self.f.read(self.columnCount*4))
        self.rowBytes = self.columnCount*4
        for i in self.colTypes:
            rowBytes += self.dataTypeSizes[i-1]
        self.tableSize = unpack("i", self.f.read(4))[0]
        self.rowCount = unpack("i", self.f.read(4))[0]
        
    def __del__(self):
        self.f.close()


# helper functions
def getStr(byt):
    return str(byt[0]).split("\\")[0][2:]

def navigate(db, row, col):
    # navigate cursor to row, col in binary file 
    # of given table object
    position = db.metaDataBytes + db.rowBytes*row
    db.f.seek(position)
    for i in range(col):
        db.f.seek(db.dataTypeSizes[db.colTypes[i]-1],1)
        db.f.seek(4,1)
        
def get(db, row, col):
    # get value at row, col of given table object
    navigate(db, row, col)
    data = unpack(specifiers[db.colTypes[col]-1], db.f.read(dataTypeSizes[db.colTypes[col]-1]))
    if db.colTypes[col] == 4:
        data = getStr(data)
    else:
        data = data[0]
    return data

def reconstruct(db, row, col):
    # reconstruct row by following pointers
    res = {}
    curRow = row
    curCol = col
    tableNumber = int(row/db.tableSize)
    for i in range(db.columnCount):
        curCol = (col + i)%db.columnCount
        res[curCol] = get(db, curRow, curCol)
        nextField = unpack("i",db.f.read(4))[0]
        curRow = tableNumber*db.tableSize + nextField
    return res
# helper functions



def find(db, col, req):
    # db: tableObj
    # req: data to be searched in col
    # returns a list of all matching fields
    res = []
    for t in range(int(db.rowCount/db.tableSize)):
        base = t*db.tableSize
        hi = db.tableSize-1
        lo = 0
        while hi>lo:
            mid = int((hi+lo)/2)
            if get(base + mid,col) < req:
                lo = mid + 1
            else:
                hi = mid
        if get(db, base + lo,col) == req:
            res.append(reconstruct(db, base + lo, col))
    for t in range(db.rowCount%db.tableSize):
        r = int(db.rowCount/db.tableSize)*db.tableSize + t
        if get(db, r, col) == req:
            res.append(reconstruct(db, base + lo, col))
    return res    

 

def read(givenTable, col, data):
    # givenTable is in the format:
    # class Table:
    # def __init__(self):
    #     self.name = ""
    #     self.col_names = {}
    #     self.metadata = []
    db = tableObj(givenTable.name)
    return find(db, col, data)

def main():
    pass

if __name__ == "__main__":
    main()