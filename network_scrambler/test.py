import subprocess
import os

for i in range(3):
    ls_output = subprocess.Popen(["python3", os.getcwd() + '/network_scrambler/network_scrambler.py', str(1)])