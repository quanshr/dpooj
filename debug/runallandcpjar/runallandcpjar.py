import threading
import time
import os, sys
import shutil
from random import sample
import json

hw = 14

tot_count = 30
if len(sys.argv) > 1:
    tot_count = int(sys.argv[1])
    print(sys.argv[1])
t = 2
n = 5
m = 100
student_count = 5

workplace_path = '../../static/workplace'
# args
num_worker = 2
std_path = f"{workplace_path}/std"
stdcode_path = f"{std_path}/code_hw{hw}"
log_path = f"{std_path}/log"

import sys
sys.path.append('../../')
from init import db, app
from models import User
#from flask_script import Manager, Shell

users = []
with app.app_context():
    allusers = User.query.all()

    for user in allusers:
        if user.is_uploaded:
            users.append(user.username)

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

users.sort()
print(users)
print(f"{len(users)} users begin to run code!")

users_path = f"{workplace_path}/users"

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

for my_count in range(tot_count):
    input_path = f"in/{my_count}.in"
    output_path = f"out/{my_count}"
    os.system(f"mkdir {output_path}")
    
    os.system(f"java -jar ../maker/maker_hw14.jar {t} {n} \
        {m} {student_count} > {input_path}")

    
    for user in users:
        os.system(f"timeout 5 java -XX:MaxNewSize=128m -jar \
            {users_path}/{user}/code_hw{hw}.jar < {input_path} > {output_path}/{user}.out")
    for user in users:
        if myhash(f"{output_path}/{user}.out") != 0:
            for user1 in users:
                if not mydiff(f"{output_path}/{user}.out", f"{output_path}/{user1}.out"):
                    same_count[user] += 1
    print(my_count)
    
mx = 0
for user in users:
    if same_count[user] > mx:
        mx = same_count[user]
    print(user, same_count[user])


cleandir(f"{std_path}/code")
std_count = 0
for user in users:
    if same_count[user] == mx:
        os.system(f"cp {users_path}/{user}/code_hw{hw}.jar {std_path}/code/{user}.jar")
        print(user)
    