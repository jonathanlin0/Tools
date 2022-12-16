# used to send out random requests in caes ISP is checking network activity

# TODO:
# - maybe add POST requests
# - start sending files

import os
import requests
import time
import random
import sys
from applescript import tell

#set what command you want to run here
# print("hi")
# print('python3 "' + os.getcwd() + '/network_scrambler/test.py"')
# yourCommand = 'python3 "' + os.getcwd() + '/network_scrambler/test.py"'

# tell.app( 'Terminal', 'do script "' + yourCommand + '"')

# time.sleep(999)

successful_requests = 0
total_requests = 0

print(os.path.dirname(__file__))

f = open(os.path.dirname(__file__) + '/common_words.txt', 'r')
common_words = f.read().splitlines()
f.close()

# prints out the program's usage
def usage():
    print("usage: python3 network_scrambler.py iterations")
    print("    iterations: the total number of requests to send out (0 for unlimited)")
    exit()

def log_request(link):
    # TODO
    pass

# get random yahoo searches
def get_yahoo():

    # part of URL that goes in front of every search
    front_stem = "https://search.yahoo.com/search?p="

    out = []

    # create a list of one word searches
    for word in common_words:
        out.append(front_stem + word)

    # create a list of two word searches
    for word in common_words:
        out.append(front_stem + word + "+" + random.choice(common_words))

    return out

# get random bing searches
def get_bing():

    front_stem = "https://www.bing.com/search?q="

    out = []

    # create a list of one word searches
    for word in common_words:
        out.append(front_stem + word)

    # create a list of two word searches
    for word in common_words:
        out.append(front_stem + word + "+" + random.choice(common_words))

    return out

def get_links():

    links = []

    links = links + get_yahoo() + get_bing()
    
    # shuffle the links
    random.shuffle(links)

    return links

# process command line arguments
if len(sys.argv) != 2:
    usage()

total_runs = 0
try:
    total_runs = int(sys.argv[1])
except:
    usage()


if total_runs == 0:
    total_runs = 9999999

links = get_links()

# get a list of random user agents
r = requests.get("https://glasstea0.pythonanywhere.com/User-Agents/")
user_agents = r.json()["User-Agents"]

# read in provided proxies from proxies.txt
f = open(os.path.dirname(__file__) + "/proxies.txt")
all_proxies = f.read().splitlines()
f.close()

links_index = 0
for i in range(total_runs):
    
    # if the index is past the length of all the links
    if links_index >= len(links):

        # reset the links_index to the beginning
        links_index = 0

        # refresh the random links list
        links = get_links()
    
    # pick random User-Agent
    headers = {
        "User-Agent": random.choice(user_agents)
    }

    # pick a random proxy
    proxy = random.choice(all_proxies)
    proxies = {
        'http': 'http://' + proxy,
        'https': 'http://' + proxy,
    }

    print("")

    try:
        # send a request to the random link
        r = requests.get(links[links_index], headers = headers, proxies = proxies, timeout = 3)

        # log the request
        f = open(os.path.dirname(__file__) + "/requested_links.txt", "a")
        f.write(links[links_index] + "\n" + str(time.time()) + "\n")

        print("Proxy: " + proxy)
        print("User-Agent: " + headers["User-Agent"])
        print("URL: " + links[links_index])

        # log any unusual codes
        if "200" not in str(r):
            f = open(os.path.dirname(__file__) + "/unusual_codes.txt", "a")
            f.write(links[links_index] + "\n" + str(r) + "\n")
            f.close()

        links_index += 1
    except:
        print("error")