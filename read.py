from importlib.metadata import entry_points
from sys import argv
from struct import unpack

# supported commands:

# find(column, required) 
#     eg. find(1, "Anthony")
#     returns all matches of key "Anthony" in column 1

# reconstruct(row, col)
#     reconstructs a particular row using one entry
#     by following pointers

# get(row, col)
#     get the entry at row, col

# printrow(k)
#     print the kth row

#global variables
dataTypeSizes = [4, 16, 1, 140]
specifiers = ["i", "f", "?", "140s"]
columnCount = 0
metaDataBytes = 0
colTypes = []
rowBytes = 0
tableSize = 0
rowCount = 0
f = open("testdb", 'rb+')

def navigate(row, col):
    # navigate cursor to row, col
    position = metaDataBytes + rowBytes*row
    f.seek(position)
    for i in range(col):
        f.seek(dataTypeSizes[colTypes[i]-1],1)
        f.seek(4,1)

def get(row, col):
    # get value at row, col
    navigate(row, col)
    data = unpack(specifiers[colTypes[col]-1], f.read(dataTypeSizes[colTypes[col]-1]))
    if colTypes[col] == 4:
        data = getStr(data)
    else:
        data = data[0]
    return data

def reconstruct(row, col):
    # first navigate to that row
    # reconstruct original row from row, col followimg pointers
    # returns a dictionary [col: data]
    res = {}
    curRow = row
    curCol = col
    tableNumber = int(row/tableSize)
    for i in range(columnCount):
        curCol = (col + i)%columnCount
        res[curCol] = get(curRow, curCol)
        next = unpack("i",f.read(4))[0]
        curRow = tableNumber*tableSize + next
    return res

def find(col, req):
    # binary search tables for
    # req data in specific col
    # returns a list of all matching rows
    res = []
    for t in range(int(rowCount/tableSize)):
        base = t*tableSize
        hi = tableSize-1
        lo = 0
        while hi>lo:
            mid = int((hi+lo)/2)
            if get(base + mid,col) < req:
                lo = mid + 1
            else:
                hi = mid
        if get(base + lo,col) == req:
            res.append(reconstruct(base + lo, col))
    for t in range(rowCount%tableSize):
        r = int(rowCount/tableSize)*tableSize + t
        if get(r, col) == req:
            res.append(reconstruct(base + lo, col))
    return res    

def findRows(A, B):
    # print all rows from A to B
    pass

def getStr(byt):
    return str(byt[0]).split("\\")[0][2:]

def printrow(row):
    position = metaDataBytes + rowBytes*row
    f.seek(position)
    res = ""
    for i in colTypes:
        data = unpack(specifiers[i-1], f.read(dataTypeSizes[i-1]))
        if i == 4:
            data = getStr(data)
        else:
            data = data[0]
        res += str(data)
        res += ","
        ptr = unpack("i", f.read(4))[0]
        res += str(ptr)
        res += ","
    print(res)


#interpret metadata
columnCount = unpack("i", f.read(4))[0]
metaDataBytes = 4 + columnCount*4 + 4 + 4
colTypes = unpack(f"{columnCount}i",f.read(columnCount*4))
rowBytes = columnCount*4
for i in colTypes:
    rowBytes += dataTypeSizes[i-1]
tableSize = unpack("i", f.read(4))[0]
rowCount = unpack("i", f.read(4))[0]

print([columnCount, rowBytes, tableSize, rowCount])
print(colTypes)
# printrow(0)
for i in range(rowCount):
    printrow(i)

print(find(3,"Buckland"))