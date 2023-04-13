import random

teachers = ['张三','李四','A','B','C','D','E','F']
offices  = [[],[],[]]

while len(teachers)>0:
    
    random_office = random.randint(0, len(offices)-1)
    if len(teachers) == 1:
        offices[random_office].append(teachers[0])
        break
    
    random_Teacher = random.randint(0, len(teachers)-1)
    offices[random_office].append(teachers[random_Teacher])
    teachers.pop(random_Teacher)

print(offices)