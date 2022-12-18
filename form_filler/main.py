from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from selenium.webdriver.chrome.options import Options
import requests
import os
from bs4 import BeautifulSoup
import random
import json
import subprocess

def get_free_responses():
    """
    Gets all the entry.x values of the free response questions of the Google Form.
    
        Parameters:
            None
        
        Returns:
            entries: a list of the entry.x values of the free response questions
    
    """

    # the script that is run in the console to retrieve the entry.x links
    js_code = """function loop(e){
    if(e.children)
        for(let i=0;i<e.children.length;i++){
            let c = e.children[i], n = c.getAttribute('name');
            if(n) console.log(`${c.getAttribute('aria-label')}: ${n}`);
            loop(e.children[i]);
        }
    }; loop(document.body);"""

    # make selenium headless
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    # option required to read the logs from js_code
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = { 'browser':'ALL' }

    # create the driver obj
    driver = webdriver.Chrome(os.path.dirname(__file__) + '/chromedriver', options=options, desired_capabilities=d)

    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfgb0u-_UkKp6iQeT-a34ZQ52EhYjb-b1uS-O1pIam8emkBgQ/viewform")
    sleep(2)

    # run the js code in the browser's console
    driver.execute_script(js_code)
    sleep(1)

    # organize the console's output after running js_script
    console_log = driver.get_log('browser')
    console_outputs = []

    for log_obj in console_log:
        console_outputs.append(log_obj["message"])

    all_entries = []
    for i in range(len(console_outputs)):
        if "entry." in console_outputs[i]:
            all_entries.append(console_outputs[i][console_outputs[i].find("null:") + 6:len(console_outputs[i]) - 1])

    # remove all the multiple choice entry.x values
    entries = []
    for ele in all_entries:
        if "_sentinel" not in ele:
            entries.append(ele)
    
    return entries

def get_multiple_choices():
    """
    Gets all the entry.x values of the multiple choice questions of the given Google Form

        Parameters:
            None
        
        Returns:
            out_dict: a dictionary where the key is the entry.x value and the value is the possible answer choices
    """

    # clean up the entry_value cause entry_value can be in format of entry.x_word instead of just entry.x
    def clean_string(raw_str):
        end_index = len(raw_str)
        for i in range(6, len(raw_str)):
            cur_str = raw_str[i:i+1]

            if cur_str.isdigit() == False:
                end_index = i
                break
                        
        return raw_str[0:end_index]
    
    r = requests.get("https://docs.google.com/forms/d/e/1FAIpQLSfgb0u-_UkKp6iQeT-a34ZQ52EhYjb-b1uS-O1pIam8emkBgQ/viewform")
    s = BeautifulSoup(r.content, 'html.parser')

    questions = s.find_all("div", {"jscontroller": "UmOCme"})

    out_dict = {

    }
        
    # get the entry.x values
    for q in questions:
            
        # object with jsname:DTMEae holds the entry.x value
        entry_value = q.find("input", {"jsname":"DTMEae"})["name"]

        entry_value = clean_string(entry_value)

        # all the possible answer choices for that question
        answer_choices = q.find_all("span", {"class":"aDTYNe snByac OvPDhc OIC90c"})

        answers_str = []
                    
        for a in answer_choices:
            answers_str.append(a.text)

        out_dict[entry_value] = answers_str
    
    return out_dict

# main_dict will get transfered to form_data.json
main_dict = {}

print("Please type the link of the Google Form you would like automatically filled out: ")
link = input("")

# correct form of link: <link>/viewform
if "viewform" not in link:
    # this will run if the google form link is in shortned form
    r = requests.get(link)
    link = r.url

# convert "viewform" tail of link to "formResponse"
# this new link is where we can directly submit form responses
link = link[:link.find("viewform")] + "formResponse"

main_dict = {
    "link": link,
    "entries":{
        "frq":get_free_responses(),
        "mcq":{}
    }
}

MCQs = get_multiple_choices()
for question in MCQs:
    main_dict["entries"]["mcq"][question] = MCQs[question]

json_obj = json.dumps(main_dict, indent = 4)
 
# Writing to sample.json
with open(os.path.dirname(__file__) + "/form_data.json", "w") as outfile:
    outfile.write(json_obj)

print("How many total forms would you like to submit?")
total_forms = input("")

try:
    total_forms = int(total_forms)
except:
    print("Error: the number of total forms was not an integer.")


print("How many threads would you like?")
total_threads = input("")

try:
    total_threads = int(total_threads)
except:
    print("Error: the number of threads was not an integer.")

# a list of all the subprocesses
sb = []

for i in range(total_threads):
    sb.append(subprocess.Popen(["python3", os.path.dirname(__file__) + '/filler.py', str(int(total_forms / total_threads))]))

errors = []

while True:
    sleep(2)
    
    complete = True
    for i in sb:
        errors.append(i.wait())
        #complete = False
    
    if complete == True:
        cnt = 0
        for e in errors:
            if e != 0:
                cnt += 1
        print("There were " + str(cnt) + " errors.")
        print("Completed")
        exit()