import os, sys

file1 = sys.argv[1]
file2 = sys.argv[2]

def myhash(file_path):
    with open(file_path, 'r') as file:
        txt = file.readlines()
    
    res = 0
    for line in txt:
        if line[0] == '[':
            for ch in line:
                res += ord(ch)
    return res
    
def diff(file1, file2):
    return myhash(file1) == myhash(file2)

myhash(file1)