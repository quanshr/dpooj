import threading
import time
import os, sys
import shutil
from random import sample
import json

hw = 14

tot_count = 20
t = 2
n = 3
m = 50
student_count = 5

workplace_path = '../static/workplace'
java_path = '../jdk8/jdk1.8.0_152/bin/java'
# args
num_worker = 2
std_path = f"{workplace_path}/std"
stdcode_path = f"{std_path}/code_hw{hw}"
log_path = f"{std_path}/log"

import sys
sys.path.append('../')
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

print(f"{len(users)} users begin to run code!")

users_path = f"{workplace_path}/users"

def myhash(file_path):
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
    os.system(f"java -jar maker/maker_hw{hw}.jar {t} {n} \
        {m} {student_count} > {input_path}")

    for user in users:
        os.system(f"timeout 10 java -XX:MaxNewSize=128m -jar \
            {users_path}/{user}/code_hw{hw}.jar < {input_path} > out/{my_count}_{user}.out")
    for user in users:
        for user1 in users:
            if not mydiff(f"out/{my_count}_{user}.out", f"out/{my_count}_{user1}.out"):
                same_count[user] += 1
                
mx = 0
for user in users:
    if same_count[user] > mx:
        mx = same_count[user]
    print(user, same_count[user])

std_path = f"{workplace_path}/std/code_hw{hw}"
std_count = 0
for user in users:
    if same_count[user] == mx:
        os.system(f"cp {users_path}/{user}/code_hw{hw}.jar {std_path}/{user}.jar")
        print(user)
    