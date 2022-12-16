import sys
import os
import requests

def usage():
    print("python3 checker.py starting_index num")
    print("    starting_index: the starting line of untested_ips.txt you want to start on")
    print("    num: the number of ips you want to check")

# process command line arguments
if len(sys.argv) != 3:
    usage()

starting_index = sys.argv[1]
num = sys.argv[2]

try:
    starting_index = int(starting_index)
    num = int(num)
except:
    usage()
    exit()

if num < 0:
    print("Error: num must be greater than 0")

f = open(os.path.dirname(__file__) + "/untested_ips.txt", 'r')
all_ips = f.read().splitlines()
f.close()

all_ips.insert(0, "")

for i in range(starting_index - 1, starting_index + num - 1):

    proxies = {
        'http': 'http://' + all_ips[i],
        'https': 'http://' + all_ips[i],
    }

    try:
        print("trying ip " + all_ips[i])
        r = requests.get("https://www.google.com/", proxies = proxies, timeout = 1)

        if "200" in str(r):
            print("200: " + all_ips[i])
            f = open(os.path.dirname(__file__) + "/working_proxies.txt", "a")
            f.write(all_ips[i] + "\n")
            f.close()
    except:
        print("error")