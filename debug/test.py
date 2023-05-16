import threading
import time
import os
import shutil
from random import sample
import json
import sys

sys.argv.append(3)

i = 0
for j in range(3):
    print(i)
    i += 1
    time.sleep(1)
    