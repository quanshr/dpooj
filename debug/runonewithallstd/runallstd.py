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
std_path = f"{workplace_path}/std"
stdcode_path = f"{std_path}/code_hw{hw}"
log_path = f"{std_path}/log"

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


stds= os.listdir(stdcode_path)
print(f"{len(stds)} stds begin to run code!")

tot_count = 1

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
for std in stds:
    same_count[std] = 0

input_path = f"in.txt"
# os.system(f"java -jar ../maker/maker_hw{hw}.jar {t} {n} \
#     {m} {student_count} > {input_path}")

for std in stds:
    os.system(f"timeout 10 java -XX:MaxNewSize=128m -jar \
        {stdcode_path}/{std} < {input_path} > out/{std}.out")
for std in stds:
    for std1 in stds:
        if not mydiff(f"out/{std}.out", f"out/{std1}.out"):
            same_count[std] += 1
                
mx = 0
for std in stds:
    if same_count[std] > mx:
        mx = same_count[std]
    print(std, same_count[std])
    

    