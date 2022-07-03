'''
Type code {   SUPPORTS ONLY THESE FOR NOW 
    1 - int 
    2 - float 
    3 - bool
    4 - str
}

metadata structure
[NUMBER_OF_COL, TYPE_CODE_1, TYPE_CODE_2, ..., TYPE_CODE_N, LIMIT, CURRENT_ENTRY_IN_NEW_TABLE]
'''

def createDB(table,metadata):
    with open (table["name"], 'w') as f:
        f.write(','.join([str(i) for i in metadata]))


def writeDB(table, metadata, row):
    limit = metadata[-2] 
    with open(table["name"],'a+') as f:
        f.write(',')
        f.write(f',{limit},'.join(row))
        f.write(f',{limit}')

    if metadata[-1] + 1 == limit:
        with open(table["name"],'r+b') as f:
            # This code will be optimized in byte mode
            # a,lim,b,lim,c,lim,
            # a,lim,b,lim,c,lim,
            # a,lim,b,lim,c,lim,
            # a,lim,b,lim,c,lim,
            # a,lim,b,lim,c,lim
            f.seek(-1,2)
            comma = 0
            comma_lit = bytes(',', 'ascii')
            while comma < limit*(metadata[0])*2:
                if f.read(1) == comma_lit: comma += 1
                f.seek(-2,1)
            f.seek(2,1)
            pos = f.tell()
            buffer = f.read().decode('ascii')
            tokens = list(filter(None,buffer.split(',')))
            last_table = [list() for i in range(metadata[0])]
            index = 0
            for i in range(limit):
                for j in range(metadata[0]):
                    last_table[j].append((tokens[index],i))
                    index+=2
            print(last_table)
            for i in range(metadata[0]):
                last_table[i].sort()

            f.seek(pos-1,0)
            for i in range(limit):
                for j in range(metadata[0]):
                    f.write(bytes(f",{last_table[j][i][0]},{last_table[j][i][1]}", "ascii"));







if __name__ == "__main__":
    data = [ "Joseph","Campbell","Isaac" "Buckland","71","2161947558","Austin.Clark@gmail.com"] 
    table = {'name':'fake.txt'}
    metadata= [6,4,4,4,1,4,4,2,0,]
    createDB(table,metadata)
    writeDB(table,metadata,data)
    # print(table)
    data = [ "Boseph","Campbell","Isaac" "Buckland","71","2161947558","Austin.Clark@gmail.com"] 
    metadata= [6,4,4,4,1,4,4,3,1,]
    writeDB(table,metadata,data)
    # print(table)
    data = [ "Joseph","Campbell","Isaac" "Buckland","71","2161947558","Austin.Clark@gmail.com"] 
    metadata= [6,4,4,4,1,4,4,3,2,]
    writeDB(table,metadata,data)
    # print(table)
