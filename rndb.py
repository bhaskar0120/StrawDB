import random
import string
from sys import argv

db = [['ani', '20', 'BHU'], ['bob', '23', 'GOOGLE'], ['alice', '19', 'STANFORD'], ['rohan', '21', 'IITKGP'], ['raj', '22', 'DELOIT'], ['yash', '26', 'BHU'], ['devansh', '22', 'BHU']]

def generate():
    data = []
    name = ''.join(random.choices(string.ascii_lowercase, k = 3 + int(10*random.random())))
    age = 16 + int(20*random.random())
    org = ''.join(random.choices(string.ascii_uppercase, k = 3 + int(10*random.random())))
    return [name, age, org]


n = 30
if len(argv)>2:
    n = argv[2]

for t in range(n):
    db.append(generate())

db.sort()

if len(argv) > 1:
    f = open(argv[1], 'w')
    for i in range(len(db)):
        for j in range(len(db[0])):
            f.write(str(db[i][j]))
            f.write(',')