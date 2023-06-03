import threading
import time
import os, sys
import shutil
from random import sample
import json

hw = 14

workplace_path = '../static/workplace'
java_path = '../jdk8/jdk1.8.0_152/bin/java'
# args
num_worker = 16
std_path = f"{workplace_path}/std"
stdcode_path = f"{std_path}/code_hw{hw}"
log_path = f"{std_path}/log"
user = sys.argv[1]
print(f"{user} begin to run code!")

user_path = f"{workplace_path}/users/{sys.argv[1]}"
result_path = f"{user_path}/result.json"

with open(f"{user_path}/runargs.json", 'r') as file:
    runargs = json.load(file)
runargs['is_running'] = 1
with open(f"{user_path}/runargs.json", 'w') as file:
    json.dump(runargs, file)
    
tot_count = runargs['num_runs']
tot_count = 2000


log_count = 0
count_lock = threading.Lock()
file_lock = threading.Lock()
now_count = 0
result_template = {'all':0, 'ac':0, 'wa':0, 're':0, 'tle':0, 'uke':0}
RE = 256
TLE = 31744
mx_err = 3
can_end = 0
std_count = len(os.listdir(stdcode_path))

print("begin")

class MyThrd(threading.Thread):
    def __init__(self , thread_id):
        super(MyThrd,self).__init__()
        self.thread_id = thread_id
        #print(f"{self.thread_id} build")
    def run(self):
        global log_count, now_count, can_end, tot_count
        while not can_end and (now_count < tot_count or tot_count == -1):
            
            with file_lock:
                with open(f"{std_path}/can_run", 'r') as file:
                    can_run = file.read()
                if can_run == "0":
                    time.sleep(1)
                    continue
            
            if num_worker == 1:
                time.sleep(2)
            
            with count_lock:
                if now_count >= tot_count:
                    break
                now_count += 1
                my_count = now_count
            input_path = f"{user_path}/input/{my_count}.in"
            os.system(f"java -jar maker/maker_hw{hw}.jar {runargs['t']} {runargs['n']} \
                {runargs['m']} {runargs['student_count']} > {input_path}")

            run_status = self.runcode(user_path, input_path, my_count)
            userout_path = f"{user_path}/output/{my_count}.out"
            stdout_path = ""

            for i in range(std_count):
                os.system(f"timeout 30 java -XX:MaxNewSize=128m -jar {stdcode_path}/code_{i}.jar < {input_path} > {user_path}/stdout/{my_count}_{i}.out")
            for i in range(std_count):
                diff_num = 0
                for j in range(std_count):
                    if os.system(f"diff {user_path}/stdout/{my_count}_{i}.out {user_path}/stdout/{my_count}_{j}.out > /dev/null"):
                        diff_num += 1
                        
                if diff_num < std_count / 2:
                    if stdout_path == "":
                        with file_lock:
                            if stdout_path == "":
                                stdout_path = f"{user_path}/stdout/{my_count}.out"
                                os.system(f"cp {user_path}/stdout/{my_count}_{i}.out {stdout_path}")
                else:
                    with file_lock:
                        print(f"file code_{i} error !!")
                        num_log = len(os.listdir(log_path))
                        os.mkdir(f"{log_path}/{num_log}_{i}")
                        os.system(f"cp {input_path} {log_path}/{num_log}_{i}/input.txt")
                        for j in range(std_count):
                            os.system(f"cp {user_path}/stdout/{my_count}_{j}.out {log_path}/{num_log}_{i}/{j}.out")
            
            if stdout_path == "":
                with count_lock:
                    if tot_count != -1:
                        tot_count += 1
                continue



            with file_lock:
                with open(result_path, 'r') as file:
                    json_data = json.load(file)
                if run_status:
                    id = json_data['all'] - json_data['ac']
                    os.system(f"cp {input_path} {user_path}/wrongdata/{id}.in")
                    os.system(f"cp {stdout_path} {user_path}/wrongdata/{id}.ans")
                    json_data['all'] += 1
                    if run_status == RE:
                        os.system(f"echo 'your code seems to be RE' > {user_path}/wrongdata/{id}.re")
                        json_data['re'] += 1                   
                    elif run_status == TLE:
                        os.system(f"echo 'your code seems to be TLE' > {user_path}/wrongdata/{id}.tle")
                        json_data['tle'] += 1                    
                    else:
                        os.system(f"echo 'there seems to be an Unknown Error with your code. \n(Error Code: {run_status})' > {user_path}/wrongdata/{id}.uke")
                        json_data['uke'] += 1
                        os.system(f"echo 'error code: {run_status}' > errorcode.txt")
                    with open(result_path, 'w') as file:
                        json.dump(json_data, file)
                    if id >= mx_err - 1:
                        can_end = 1
                
                else:
                    is_wrong = os.system(f"diff {userout_path} {stdout_path} > /dev/null")
                    
                    if is_wrong:
                        id = json_data['all'] - json_data['ac']
                        os.system(f"cp {userout_path} {user_path}/wrongdata/{id}.out")
                        os.system(f"cp {input_path} {user_path}/wrongdata/{id}.in")
                        os.system(f"cp {stdout_path} {user_path}/wrongdata/{id}.ans")
                        os.system(f"diff {userout_path} {stdout_path} > {user_path}/wrongdata/{id}.diff")
                        if id >= mx_err - 1:
                            can_end = 1

                    json_data['all'] += 1
                    json_data['ac'] += 0 if is_wrong else 1
                    json_data['wa'] += 1 if is_wrong else 0
                    with open(result_path, 'w') as file:
                        json.dump(json_data, file)

            os.system(f"rm {input_path}")
            os.system(f"rm {stdout_path}")
            os.system(f"rm {userout_path}")

    def runcode(self, user_path, input_path, my_count):
        r = os.system(f"timeout 15 java -XX:MaxNewSize=128m -jar {user_path}/code_hw{hw}.jar < {input_path} > {user_path}/output/{my_count}.out 2> /dev/null")
        if r == RE:
            r = os.system(f"timeout 15 {java_path} -XX:MaxNewSize=128m -jar {user_path}/code_hw{hw}.jar < {input_path} > {user_path}/output/{my_count}.out")

def cleandir(name):
    if os.path.isdir(name):
        shutil.rmtree(name)
    os.mkdir(name)

def cleanfile(name):
    if os.path.exists(name):
        os.system(f"rm {name}")
    os.system(f"touch {name}")

cleandir(f"{user_path}/input")
cleandir(f"{user_path}/output")
cleandir(f"{user_path}/wrongdata")
cleandir(f"{user_path}/stdout")
cleanfile(result_path)
with open(result_path, 'w') as file:
    json.dump(result_template, file)
if not os.path.exists(log_path):
    os.mkdir(log_path)

    
threads = []
for i in range(num_worker):
    thread = MyThrd(i)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
    
print(f"finish run :{sys.argv[1]}, {now_count}")

runargs['is_running'] = 0
with open(f"{user_path}/runargs.json", 'w') as file:
    json.dump(runargs, file)
    

with open(result_path, 'r') as file:
    json_data = json.load(file)
if json_data['all'] == json_data['ac']:
    print(f"\033[1m\033[32m{user}: {json_data}\033[0m")
else:
    print(f"\033[1m\033[31m{user}: {json_data}\033[0m")
    

    