from random import sample, choices, randint
from sys import argv

first_names = [ "Andrew", "Anthony", "Austin", "Benjamin", "Blake", "Boris", "Isaac", "Jack", "Jacob", "Jake", "James", "Jason", "Joe", "John", "Jonathan", "Joseph", "Joshua", "Julian", "Justin", "Keith", "Kevin", "Leonard"]

last_names = [ "Bailey",  "Ball", "Bell", "Berry", "Black", "Blake", "Bond", "Bower", "Brown", "Buckland", "Burgess", "Butler", "Cameron", "Campbell", "Carr", "Chapman", "Churchill", "Clark", "Clarkson", "Coleman", "Cornish", "Davidsonk" ]

def first(count):
    global first_names
    return sample(first_names, count)

def last(count):
    global last_names
    return sample(last_names, count)

def email(count):
    global last_names, first_names
    return [f"{i}.{j}@gmail.com" for i,j in zip(sample(first_names,count), sample(last_names,count))]

def full(count):
    global last_names, first_names
    return [f"{i} {j}" for i,j in  zip(sample(first_names,count), sample(last_names,count))]

def phone(count):
    l = [str(i) for i in range(10)]
    return [''.join(choices(l,k=10)) for i in range(count)]

def age(count):
    return [str(randint(3,80)) for i in range(count)]

def main():
    if argv[1] == "--help":
        print("""
        py faker.py <optional: filename>

        Edit the variable name `template` in the file according to the template
        You can change the template in any way you like 

        #template keywords: [first, last, full, age, phone, email, (number of rows)]
        
        Max number of names = 22
        """)
        return



    #template keywords: [first, last, full, age, phone, email, (number of rows)]
    #22 Unique names available

    template = [first , last ,full, age, phone, email, 3]

    n = min(template.pop(),22);
    ret= []
    for j in template:
        ret.append(j(n))

    if len(argv) < 2:
        for i in range(n):
            for j in range(len(template)):
                print(ret[j][i],end=",");
            print()
    else:
        with open(argv[1],'w') as f:
            for i in range(n):
                for j in range(len(template)):
                    f.write(ret[j][i]+",");



if __name__ == "__main__":
    main()
