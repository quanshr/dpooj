import threading
import time
import os, sys
import shutil
from random import sample
import json

hw = 14

t = 2
n = 3
m = 20
student_count = 5

sys.path.append('../../')

workplace_path = '../../static/workplace'
java_path = '../../dk8/jdk1.8.0_152/bin/java'
# args
num_worker = 2
user_path = f"{workplace_path}/users"
log_path = f"{user_path}/log"

from init import db, app
from models import User
#from flask_script import Manager, Shell

def cleandir(name):
    if os.path.isdir(name):
        shutil.rmtree(name)
    os.mkdir(name)

def cleanfile(name):
    if os.path.exists(name):
        os.system(f"rm {name}")
    os.system(f"touch {name}")

cleandir("in")
cleandir("out")

users = []
for user in os.listdir(user_path):
    if os.path.exists(f"{user_path}/{user}/code_hw14.jar"):
        users.append(user)
print(f"{len(users)} users begin to run code!")

tot_count = 1

def clearstate(file_path):
    with open(file_path, 'r') as file:
        txt = file.readlines()
    
    for line in txt:
        if line.startswith('(State)'):
            txt.remove(line)
    
    with open(file_path, 'w') as file:
        file.writelines(txt)

def myhash(file_path):
    clearstate(file_path)
    
    with open(file_path, 'r') as file:
        txt = file.readlines()
    
    res = 0
    for line in txt:
        if line[0] == '[':
            for ch in line:
                res += ord(ch)
    return res
    
def mydiff(file1, file2):
    return myhash(file1) != myhash(file2)

same_count = {}
for user in users:
    same_count[user] = 0

input_path = f"in.txt"
# os.system(f"java -jar ../maker/maker_hw{hw}.jar {t} {n} \
#     {m} {student_count} > {input_path}")

for user in users:
    os.system(f"timeout 10 java -XX:MaxNewSize=128m -jar \
        {user_path}/{user}/code_hw14.jar < {input_path} > out/{user.split('.')[0]}.out")
for user in users:
    for user1 in users:
        if not mydiff(f"out/{user.split('.')[0]}.out", f"out/{user1.split('.')[0]}.out"):
            same_count[user] += 1
                
mx = 0
for user in users:
    if same_count[user] > mx:
        mx = same_count[user]
    print(user, same_count[user])
    