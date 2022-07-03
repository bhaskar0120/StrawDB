from struct import pack
from main import Table

type_ref_table = { 1:"i", 2:"f", 3:"?" }
size_table = { 1:4, 2:4, 3:1, 4:140 }

def strFill(text):
    if len(text) > 140:
        text = text[:140]
        return text
    return ''.join([text,'\x00'*(140-len(text))])

def createDB(table):
    names = []
    for val in table.col_names.keys():
        names.append(strFill(val))
    with open (table.name, 'wb') as f:
        f.write(pack(f"{len(table.metadata)}i",*table.metadata))
        for i in names:
            f.write(bytes(i,'utf-8'))


def writeDB(table, row):
    limit = table.metadata[-2] 
    col = table.metadata[0]

    row_bytes = []
    for i,val in enumerate(row):
        if table.metadata[i+1] == 4:
            row_bytes.append(bytes(strFill(val),'utf-8'))
        else:
            row_bytes.append( pack(type_ref_table[ table.metadata[i+1] ], val) )

    with open(table.name, 'ab') as f:
        for i in row_bytes:
            f.write(i)
            f.write( pack( 'i',table.metadata[-1]%limit ) )

    table.metadata[-1]+=1
    to_curr = (len(table.metadata)-1 ) *4
    with open(table.name,'r+b') as f:
        f.seek(to_curr)
        f.write(pack('i',table.metadata[-1]))
    
    if table.metadata[-1]%limit == 0:
        row_size = 0
        for i in range(col):
            row_size += size_table[table.metadata[i+1]] + 4
        with open(table.name,'r+b') as f:
            f.seek(-row_size*limit,2)
            tb = [list() for i in range(col)]
            switch = [[-1]*col for i in range(limit)]
            for i in range(limit):
                for j in range(col):
                    readdata = f.read(size_table[table.metadata[j+1]])
                    tb[j].append((readdata, i))
                    f.seek(4,1)
            for i in range(col):
                tb[i].sort()
            for i in range(col):
                for j in range(limit):
                    switch[tb[i][j][1]][i] = j
            f.seek(-row_size*limit,2)
            for i in range(limit):
                for j in range(col):
                    f.write(tb[j][i][0])
                    next_p = switch[tb[j][i][1]][(j+1)%col]
                    f.write(pack('i',next_p))



if __name__ == "__main__":
    table = Table()
    table.name = 'fake.txt'
    table.metadata = [3,1,1,4,5,0]
    table.col_names = {"Age":0,"Age2":1, "Name":2}
    
    createDB(table)
    writeDB(table, [14,5,"Elpha"])
    writeDB(table, [12,4,"Dlpha"])
    writeDB(table, [11,3,"Clpha"])
    writeDB(table, [13,2,"Blpha"])
    writeDB(table, [10,1,"Alpha"])

    print('''
    [14,5,"Elpha"]
    [12,4,"Dlpha"]
    [11,3,"Clpha"]
    [13,2,"Blpha"]
    [10,1,"Alpha"]
    ''')
