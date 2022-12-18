import json
import os
import requests
import random
import sys

json_obj = {}

# Opening JSON file
with open(os.path.dirname(__file__) + '/form_data.json', 'r') as openfile:
 
    # Reading from json file
    json_obj = json.load(openfile)
 
entries = {}

# add the responses for the frqs
for entry in json_obj["entries"]["frq"]:
    
    # can create random sentence generator in future
    random_word = "test"
    
    entries[entry] = entries

# add the responses for the mcqs
for entry in json_obj["entries"]["mcq"]:
    entries[entry] = random.choice(json_obj["entries"]["mcq"][entry])

total_iterations = 0

try:
    # the first command line argumnt is the total number of iteration
    total_iterations = int(sys.argv[1])
except:
    print("Usage: python3 filler.py iterations")
    print("    iterations: the total number of forms you want filled for this thread.")
    exit()

for i in range(total_iterations):
    try:
        r = requests.post(json_obj["link"], data = entries)
    except Exception as e: print(e)