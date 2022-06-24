from random import random, choices, randint, sample
from struct import pack
from sys import argv

first_names = [ "Andrew", "Anthony", "Austin", "Benjamin", "Blake", "Boris", "Isaac", "Jack", "Jacob", "Jake", "James", "Jason", "Joe", "John", "Jonathan", "Joseph", "Joshua", "Julian", "Justin", "Keith", "Kevin", "Leonard"]

last_names = [ "Bailey",  "Ball", "Bell", "Berry", "Black", "Blake", "Bond", "Bower", "Brown", "Buckland", "Burgess", "Butler", "Cameron", "Campbell", "Carr", "Chapman", "Churchill", "Clark", "Clarkson", "Coleman", "Cornish", "Davidsonk" ]

def first(count,File=False):
    global first_names
    t = choices(first_names, k=count)
    if File:
        return [bytes("{}{}".format(i,"\x00"*(140-len(i))),'utf-8') for i in t]
    return t

def last(count,File=False):
    global last_names
    t =  choices(last_names, k=count)
    if File:
        return [bytes("i{}".format("\x00"*(140-len(i))),'utf-8') for i in t]
    return t

def email(count,File=False):
    global last_names, first_names
    t =  [f"{i}.{j}@gmail.com" for i,j in zip(choices(first_names,k=count), choices(last_names,k=count))]
    if File:
        return [bytes("i{}".format("\x00"*(140-len(i))),'utf-8') for i in t]
    return t

def full(count,File=False):
    global last_names, first_names
    t =  [f"{i} {j}" for i,j in  zip(choices(first_names,k=count), choices(last_names,k=count))]
    if File:
        return [bytes("i{}".format("\x00"*(140-len(i))),'utf-8') for i in t]
    return t

def phone(count,File=False):
    l = [str(i) for i in range(10)]
    t =  [''.join(choices(l,k=10)) for i in range(count)]
    if File:
        return [bytes("i{}".format("\x00"*(140-len(i))),'utf-8') for i in t]
    return t

def age(count,File=False):
    t =  [randint(3,80) for i in range(count)]
    if File:
        return [pack(f"i",i) for i in t]
    return t

    

def number(count,File=False):
    t = [random() for i in range(count)]
    if File:
        return [pack(f"f",i) for i in t]
    return t


def boolean(count,File=False):
    t =  [random() < 0.5 for i in range(count)]
    if File:
        return [pack(f"?",i) for i in t]
    return t

def main():
    if len(argv) > 1 and argv[1] == "--help":
        print("""
        py faker.py <optional: filename>

        Edit the variable name `template` in the file according to the template
        You can change the template in any way you like 

        #template keywords: [first, last, full, age, phone, email, number, boolean, (number of rows)]
        
        """)
        return
    File = False
    if len(argv) > 1:
        File = True



    #template keywords: [first, last, full, age, phone, email, number, boolean (number of rows)]

    #template = [first , last ,full, age, phone, email, number,boolean, 29]
    # template = [age, age, age, 7]
    template = [first, first, age, 104]
    limit = 10


    types = {first:4, last:4, age:1, phone:4,email:4, full:4, number:2, boolean:3}
    formatter = {first:'s', last:4, age:1, phone:4,email:4, full:4, number:2, boolean:3}
    n = template.pop()
    metadata = [len(template)]
    metadata += [types[i] for i in template]
    metadata.append(limit)
    metadata.append(n)


    print(metadata)
    ret= []
    down = [(i+1)%limit for i in range(limit)]
    up = [(i+4)%limit for i in range(limit)]
    same = list(range(limit))

    q = n%limit
    down_n =  [(i+1)%q for i in range(q)]
    up_n =  [(i+q-1)%q for i in range(q)]
    same_n= list(range(q))

    for num,j in enumerate(template):
        t = j(n,File=File)
        for i in range(limit, n+1, limit):
            t[i-limit:i] = sorted(t[i-limit:i])
        ret.append(t)

        pointer = []
        if len(template) > 2 and num == 0:
            pointer = down
            pointer = pointer*(n//limit)
            pointer += down_n
        elif len(template) > 2 and num == len(template)-1:
            pointer = up
            pointer = pointer*(n//limit)
            pointer += up_n
        else: 
            pointer = same
            pointer = pointer*(n//limit)
            pointer +=  same_n
        if File:
            pointer = [pack("i",i) for i in pointer]
            ret.append(pointer)
        else:
            ret.append(pointer)

    
    if len(argv) < 2:
        for i in metadata:
            print(i,end=',')
        print()
        for i in range(n):
            for j in range(len(ret)):
                print(str(ret[j][i]),end=",");
            print()
    else:
        with open(argv[1],'wb') as f:
            metadata = pack(f"{len(metadata)}i",*metadata)
            f.write(metadata)
            for i in range(n):
                for j in range(len(ret)):
                    f.write(ret[j][i])



if __name__ == "__main__":
    main()
