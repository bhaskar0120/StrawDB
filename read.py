from sys import argv
from struct import unpack

# todo:
# implement UB, LB: [1, 2, 2, 3, 4]
# query [datap1 datap2]

# table object
class tableObj:
    def __init__(self, table):
        self.dataTypeSizes = [4, 4, 1, 140]
        self.specifiers = ["i", "f", "?", "140s"]
        self.f = open(table,'rb+')
        self.columnCount = unpack("i", self.f.read(4))[0]
        self.metaDataBytes = 4 + self.columnCount*4 + 4 + 4
        self.colTypes = unpack(f"{self.columnCount}i",self.f.read(self.columnCount*4))
        self.rowBytes = self.columnCount*4
        for i in self.colTypes:
            self.rowBytes += self.dataTypeSizes[i-1]
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
    position = db.metaDataBytes + db.rowBytes*row + 140*db.columnCount
    db.f.seek(position)
    for i in range(col):
        db.f.seek(db.dataTypeSizes[db.colTypes[i]-1],1)
        db.f.seek(4,1)
        
def get(db, row, col):
    # get value at row, col of given table object
    navigate(db, row, col)
    data = unpack(db.specifiers[db.colTypes[col]-1], db.f.read(db.dataTypeSizes[db.colTypes[col]-1]))
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


def upperbound(db, lo, hi, col, req):
    while hi>lo:
        mid=int((hi+lo)/2)
        if mid<db.rowCount and get(db,mid,col)<=req:
            lo=mid+1
        else:
            hi=mid
    return lo

def lowerbound(db, lo, hi, col, req):
    while hi>lo:
        mid=int((hi+lo)/2)
        if mid<db.rowCount and get(db,mid,col)<req:
            lo=mid+1
        else:
            hi=mid
    return lo

def find(db, col, req):
    # db: tableObj
    # req: data to be searched in col
    # returns a list of all matching fields
    res = []
    for t in range(int(db.rowCount/db.tableSize)):
        base = t*db.tableSize
        hi = db.tableSize-1+base
        lo = base
        lb = lowerbound(db, lo, hi, col, req)
        ub = upperbound(db, lo, hi, col, req)
        if lb<db.rowCount and get(db,lb,col) == req:
            for j in range(lb, ub):
                res.append(reconstruct(db,j,col))
    
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

class __test:
    pass

def main():
    tb=__test()
    tb.name="dsgkdshd"
    print(read(tb, 0, 10))
    print(read(tb, 1,"James"))
    print(read(tb, 2, "Clarkson"))
    pass

if __name__ == "__main__":
    main()
    
# [0, 'Austin', 'Clarkson', 80]
# [1, 'Jason', 'Bond', 61]
# [2, 'Jonathan', 'Ball', 63]
# [3, 'Leonard', 'Clarkson', 31]
# [4, 'Jacob', 'Burgess', 36]
# [5, 'John', 'Cornish', 88]
# [6, 'Kevin', 'Black', 39]
# [7, 'Julian', 'Davidsonk', 54]
# [8, 'Kevin', 'Campbell', 26]
# [9, 'James', 'Ball', 42]
# [10, 'James', 'Buckland', 65]
# [11, 'Joshua', 'Churchill', 16]
# [12, 'Jack', 'Blake', 83]
# [13, 'Joshua', 'Bond', 44]
# [14, 'James', 'Buckland', 99]
# [15, 'Austin', 'Butler', 49]
# [16, 'Andrew', 'Bell', 39]
# [17, 'Jake', 'Cornish', 2]
# [18, 'Jonathan', 'Chapman', 18]
# [19, 'Justin', 'Churchill', 75]
# [20, 'Keith', 'Blake', 40]
# [21, 'John', 'Bond', 28]
# [22, 'Jack', 'Clarkson', 78]
# [23, 'Joseph', 'Black', 85]
# [24, 'Jacob', 'Churchill', 2]
# [25, 'Joe', 'Bell', 41]
# [26, 'Kevin', 'Black', 7]
# [27, 'Benjamin', 'Cornish', 85]
# [28, 'Andrew', 'Campbell', 12]
# [29, 'Joseph', 'Buckland', 66]
# [4, 1, 4, 4, 1, 7, 30]