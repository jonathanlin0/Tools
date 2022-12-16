from bs4 import BeautifulSoup
import requests
from time import sleep
import os

all_ips = []

# scraped from https://free-proxy-list.net/
def collect_1():

    print("Collecting proxies from https://free-proxy-list.net/")

    r = requests.get("https://free-proxy-list.net/")
    s = BeautifulSoup(r.content, 'html.parser')

    ip_table = s.find("table", {"class":"table table-striped table-bordered"})

    table_rows = list(ip_table.findChildren('tr'))
    
    # removes the head of the table
    table_rows.pop(0)

    ips = []

    for row in table_rows:
        ips.append(row.findChildren()[0].getText())
    
    print("Collected " + str(len(ips)) + " proxies from https://free-proxy-list.net/")

    return ips
    
# documentation of API: https://docs.proxyscrape.com/?_ga=2.94699996.1326438467.1671152344-395372277.1671152344
def collect_2():

    print("Collecting proxies from https://proxyscrape.com/")

    r = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")

    ips = r.text.splitlines()

    print("Collected " + str(len(ips)) + " proxies from https://proxyscrape.com/")

    return ips

# proxies collected from https://www.geonode.com/free-proxy-list/
# ROOM FOR EXPANSION
def collect_3():
    # anonymity level: elite, anonymous

    ips = []

    links = [
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=2&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=3&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=4&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=5&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous"
    ]

    responses = []

    for i in range(len(links)):
        print("Collecting proxies from page " + str(i + 1) + " of https://www.geonode.com/free-proxy-list/")
        responses.append(requests.get(links[i]))

    for response in responses:

        r = response
        data = r.json()["data"]

        for ele in data:
            ips.append(ele["ip"])

    print("Collected " + str(len(ips)) + " proxies from https://www.geonode.com/free-proxy-list/")

    return ips

# proxies collected from https://hidemy.name/en
# ROOM FOR EXPANSION
def collect_4():

    ips = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    links = [
        "https://hidemy.name/en/proxy-list/#list",
        "https://hidemy.name/en/proxy-list/?start=64#list",
        "https://hidemy.name/en/proxy-list/?start=128#list",
        "https://hidemy.name/en/proxy-list/?start=192#list",
        "https://hidemy.name/en/proxy-list/?start=256#list",
    ]

    responses = []

    for i in range(len(links)):
        print("Collecting proxies from page " + str(i + 1) + " of https://hidemy.name/en")
        responses.append(requests.get(links[i], headers = headers))

    for response in responses:
        s = BeautifulSoup(response.content, 'html.parser')

        ip_table = s.find("div", {"class":"table_block"})

        table_rows = list(ip_table.findChildren('tr'))
        
        for ele in table_rows:
            ips.append(ele.findChildren()[0].getText())
    
    print("Collected " + str(len(ips)) + " proxies from https://hidemy.name/en")

    return ips

# proxies scraped from https://spys.one/en/free-proxy-list/
def collect_5():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    r = requests.get("https://spys.one/en/free-proxy-list/", headers = headers)
    s = BeautifulSoup(r.content, 'html.parser')

    all_rows = list(s.findChildren('tr'))

    ip_rows = []

    for i in range(len(all_rows)):
        # only the last 30 rows are IPs
        if len(all_rows) - i <= 30:
            ip_rows.append(all_rows[i])

    ips = []

    for ele in ip_rows:
        row = ele.findChildren('td')

        if len(row) > 0 and len(ele.findChildren('font')) > 0:
            ips.append(row[0].getText())
    
    print("Collected " + str(len(ips)) + " proxies from https://spys.one/en/free-proxy-list/")

    return ips
    
all_ips = all_ips + collect_1() + collect_2() + collect_3() + collect_4() + collect_5()

# convert list of all_ips to string
out = ""
for ip in all_ips:
    out = out + ip + "\n"
out = out[:len(out) - 1]

# write all the ips to untested_ips.txt
f = open(os.path.dirname(__file__) + "/untested_ips.txt", "w")
f.write(out)
f.close()