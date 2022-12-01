from _datetime import datetime
import random
import hashlib
import sys
import re



row_data = dict()
for t in ['post', 'comment','user']:
    row_data[t] = t

#print(row_data)
# for x,y in row_data.items():
#     print(x)
#     print(y)

date_string = '2021-09-28 16:50:48'
x = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
print(x.strftime("%d/%m/%Y"))
#get now
x = datetime.now()
y = x.strftime('%Y-%m-%d %H:%M:%S')
print(y)

def create_pword_hash(length=10):

    alphabet = range(ord('A'), ord('Z'))
    pword = ""
    for x in range(0, length):
        pword += chr(random.randint(ord('A'),ord('Z')))
    print(pword)
    h = hashlib.md5(pword.encode())
    hash = h.hexdigest()
    print(hash)
    print(type(hash))
    return pword , hash

def check_password(pword, hash):
    h = hashlib.md5(pword.encode())
    if hash == h.hexdigest():
        return True
    else:
        return False

my_string= "hello \ngoodbye"
new_string = "<p>" + my_string.replace("\n", "</p><p>") + "</p>"
print(my_string)
print(new_string)
print(sys.path)

list_tup=[(1,), (2,), (3,)]
x = re.findall(r"[0-9]+", str(list_tup))
print(x)



#p,h = create_pword_hash()
#print(check_password(p,h))