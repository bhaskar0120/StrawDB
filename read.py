# Type code {   SUPPORTS ONLY THESE FOR NOW 
#     1 - int 
#     2 - float 
#     3 - bool
#     4 - str
# }

# metadata structure
# [NUMBER_OF_COL, TYPE_CODE_1, TYPE_CODE_2, ..., TYPE_CODE_N, LIMIT, CURRENT_ENTRY_IN_NEW_TABLE]

# aaaaaAAAAAAaAAAaaaAAAAAAAaaaa

from sys import argv
from struct import unpack
from turtle import pos


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


# template = [first, last, age, email, 100]
# str str int str
# meta: [int, [template: str str int str], [int, int]]
#

def navigate(row, col):
    # navigate cursor to row, col
    position = metaDataBytes + rowBytes*row
    f.seek(position)
    for i in range(col):
        f.seek(dataTypeSizes[colTypes[i]-1],1)
        f.seek(4,1)

def recon(row, col):
    # first navigate to that row
    # reconstruct original row from row, col followimg pointers

    # [...................]
    res = {}
    curRow = row
    curCol = col
    tableNumber = int(row/tableSize)
    for i in range(columnCount):
        curCol = (col + i)%columnCount
        navigate(curRow,curCol)
        data = unpack(specifiers[colTypes[curCol]-1], f.read(dataTypeSizes[colTypes[curCol]-1]))
        if colTypes[curCol] == 4:
            data = getStr(data)
        else:
            data = data[0]
        res[curCol] = data
        next = unpack("i",f.read(4))[0]
        curRow = tableNumber*tableSize + next
    
    return res

def find(col, req):
    # binary search tables for
    # req data in specific col

    pass

def getStr(byt):
    return str(byt[0]).split("\\")[0][2:]

def printrow(row):
    position = metaDataBytes + rowBytes*row
    # print("position: " + str(position))
    f.seek(position)
    res = ""
    for i in colTypes:
        data = unpack(specifiers[i-1], f.read(dataTypeSizes[i-1]))
        f.seek(4,1)
        if i == 4:
            data = getStr(data)
        else:
            data = data[0]
        res += str(data)
        res += ","
        # print(f.tell())
    print(res)


#interpret metadata
columnCount = unpack("i", f.read(4))[0]
metaDataBytes = 4 + columnCount*4 + 4 + 4
colTypes = unpack(f"{columnCount}i",f.read(columnCount*4))
rowBytes = columnCount*4
for i in colTypes:
    rowBytes += dataTypeSizes[i-1]
print(columnCount)
tableSize = unpack("i", f.read(4))[0]
rowCount = unpack("i", f.read(4))[0]

# for i in range(rowCount):
#     printrow(i)

print(recon(55,1))