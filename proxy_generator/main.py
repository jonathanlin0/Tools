from applescript import tell
import os
from time import sleep
import subprocess

print("How many threads would you like?")
print("Recommendations:")
print("    50 - low end laptop")
print("    150 - decent laptop")
print("    300+ - high end pc")
windows = input("")

try:
    windows = int(windows)
except:
    print("Error: You must input an integer for the number of windows.")
    exit()

# read in all the untested ips
f = open(os.path.dirname(__file__) + "/untested_ips.txt")
all_ips = f.read().splitlines()
f.close()

# reset the working ip text file
f = open(os.path.dirname(__file__) + "/working_proxies.txt", "w")
f.write("")
f.close()

total_length = len(all_ips)

# truncate the remainder ips
ips_per_window = int(total_length / windows)

cmd = "python3 " + os.path.dirname(__file__) + "/checker.py"

sb = []

for i in range(windows):

    starting_index = i + 1
    starting_index = starting_index * ips_per_window

    sb.append(subprocess.Popen(["python3", os.getcwd() + '/proxy_generator/checker.py', str(starting_index), str(ips_per_window)]))

errors = []

while True:
    sleep(2)
    
    complete = True
    for i in sb:
        if i.wait() != 0:
            errors.append(i.wait())
            complete = False
    
    if complete == True:
        print("There were " + str(len(errors)) + " errors.")
        print("Completed")
        exit()