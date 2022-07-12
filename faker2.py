from main import Table
from write import writeDB, createDB
from random import random

first_names = [ "Andrew", "Anthony", "Austin", "Benjamin", "Blake", "Boris", "Isaac", "Jack", "Jacob", "Jake", "James", "Jason", "Joe", "John", "Jonathan", "Joseph", "Joshua", "Julian", "Justin", "Keith", "Kevin", "Leonard"]
last_names = [ "Bailey",  "Ball", "Bell", "Berry", "Black", "Blake", "Bond", "Bower", "Brown", "Buckland", "Burgess", "Butler", "Cameron", "Campbell", "Carr", "Chapman", "Churchill", "Clark", "Clarkson", "Coleman", "Cornish", "Davidsonk" ]

def serial():
    pass
def phone():
    pass
def email():
    pass
def boolean():
    pass
def number():
    pass
def first():
    return first_names[int(random()*len(first_names))]

def last():
    return last_names[int(random()*len(last_names))]

def age():
    return int(100*random())

types = {serial:1, first:4, last:4, age:1, phone:4,email:4, number:2, boolean:3}
colNames = {serial:"serial", first:"first", last:"last", age:"age", phone:"phone",email:"email", number:"number", boolean:"boolean"}

def randomEntry(count,template=[first, last, age]):
    res = [count]
    for func in template:
        res.append(func())
    return res

def randDB(rowCount, template=[first,last,age]):
    res = []
    for i in range(rowCount):
        res.append(randomEntry(i, template))
    return res

def faker(name, rowCount, limit, template=[first,last,age]):
    db = randDB(rowCount, template)
    metadata = [len(template)+1, 1] + [types[i] for i in template] + [limit, 0]
    print([types[i] for i in template])
    table = Table()
    table.name = name
    table.metadata = metadata
    table.col_names = {"serial":0}
    curCt = {}
    for f in template:
        curCt[colNames[f]]=0
        
    for i in range(len(template)):
        f = template[i]
        curName = colNames[f] + str(curCt[colNames[f]])
        curCt[colNames[f]]+=1
        table.col_names[curName] = i+1
    
    print(table.col_names)
    print(table.metadata)
    print(table.name)
    createDB(table)
    for row in db:
        print(row)
        writeDB(table, row)
    print(table.metadata)
        
# use like: faker(name of database, rowcount, tablesize, template)
# template defaults to [first, last, age]
# note that serial column is auto added, you dont have to include it in template
faker("dsgkdshd", 30, 7)