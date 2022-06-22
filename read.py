from sys import argv

def read(col, data, db):
    # assuming that col is sorted
    lo = 0
    hi = len(db)-1
    while hi>lo:
        mid = int((hi+lo)/2)
        if db[mid][col] < data:
            lo = mid + 1
        else:
            hi = mid
    return db[lo]

def main():
    f = open("dtb.txt", 'r+')
    _db = f.readlines()
    _db = _db[0].split(',')
    db = []
    for i in range(int(len(_db)/3)):
        db.append([_db[3*i], _db[3*i+1], _db[3*i+2]])
    print(db)
    [col, req] = input().split()
    col = int(col)
    print(read(col, req, db))

if __name__ == "__main__":
    main()