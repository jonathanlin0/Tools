from applescript import tell
import os
import subprocess
from time import sleep
import time

#set what command you want to run here
cmd = 'python3 ' + os.getcwd() + '/network_scrambler/network_scrambler.py'

print("How many processes would you like to run? The more processes, the more computing power used.")
processes = input("")

try:
    processes = int(processes)
except:
    print("Error: The given input is not an integer.")
    exit()

print("How many iterations would you like per window: ")
iterations_per_window = input("")

try:
    iterations_per_window = int(iterations_per_window)
except:
    print("Error: The given input is not an integer.")
    exit()

print("Sending " + str(processes * iterations_per_window) + " randomized requests...")

#hi = subprocess.Popen(["python3", os.getcwd() + '/network_scrambler/test.py', str(processes), str(iterations_per_window)])

sb = []

for i in range(processes):

    #ls_output = subprocess.Popen(["python3", os.path.dirname(__file__) + "/test.py"])

    #ls_output = subprocess.Popen(["python3", os.getcwd() + '/network_scrambler/network_scrambler.py', str(iterations_per_window)])
    sb.append(subprocess.Popen(["python3", os.getcwd() + '/network_scrambler/network_scrambler.py', str(iterations_per_window)]))
    # subprocess.call(["python3", os.getcwd() + '/network_scrambler/test.py', str(processes), str(iterations_per_window)])

    #tell.app( 'Terminal', 'do script "' + cmd + " " + str(iterations_per_window) + '"')

# exit_codes = [p.wait() for p in pp]

sleep(3)
while True:
    sleep(2)
    
    complete = True
    for i in sb:
        if i.wait() != 0:
            complete = False
    
    if complete == True:
        print("Successfully sent " + str(processes * iterations_per_window) + " random requests.")
        exit()