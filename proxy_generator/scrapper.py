from signal import SIG_DFL
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
        
        cur_children = row.findChildren()

        proxy_anon = cur_children[4].getText()
        proxy_ip = cur_children[0].getText()
        proxy_port = cur_children[1].getText()

        if "transparent" not in proxy_anon:
            ips.append(proxy_ip + ":" + proxy_port)
    
    print("Collected " + str(len(ips)) + " proxies from https://free-proxy-list.net/")

    return ips
    
# documentation of API: https://docs.proxyscrape.com/?_ga=2.94699996.1326438467.1671152344-395372277.1671152344
def collect_2():

    print("Collecting proxies from https://proxyscrape.com/")

    r = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous,elite")

    ips = r.text.splitlines()

    print("Collected " + str(len(ips)) + " proxies from https://proxyscrape.com/")

    return ips

# proxies scraped from https://www.geonode.com/free-proxy-list/
# ROOM FOR EXPANSION
def collect_3():

    print("Collecting proxies from https://www.geonode.com/free-proxy-list/")
    # anonymity level: elite, anonymous

    ips = []

    links = [
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=2&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=3&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=4&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=5&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=6&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=7&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=8&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=9&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite&anonymityLevel=anonymous",
    ]

    responses = []

    for i in range(len(links)):
        print("Collecting proxies from page " + str(i + 1) + " of https://www.geonode.com/free-proxy-list/")
        responses.append(requests.get(links[i], timeout = 2))

    for response in responses:

        r = response
        data = r.json()["data"]

        for ele in data:
            ips.append(ele["ip"])

    print("Collected " + str(len(ips)) + " proxies from https://www.geonode.com/free-proxy-list/")

    return ips

# proxies scraped from https://www.proxy-list.download/
def collect_4():

    print("Collecting proxies from https://www.proxy-list.download/")

    links = [
        "https://www.proxy-list.download/api/v1/get?type=http&anon=elite&country=US",
        "https://www.proxy-list.download/api/v1/get?type=https&anon=elite&country=US",
        "https://www.proxy-list.download/api/v1/get?type=socks4&anon=elite&country=US",
        "https://www.proxy-list.download/api/v1/get?type=socks5&anon=elite&country=US",
        "https://www.proxy-list.download/api/v1/get?type=http&anon=anonymous&country=US",
        "https://www.proxy-list.download/api/v1/get?type=https&anon=anonymous&country=US",
        "https://www.proxy-list.download/api/v1/get?type=socks4&anon=anonymous&country=US"
        "https://www.proxy-list.download/api/v1/get?type=socks5&anon=anonymous&country=US"
    ]

    ips = []

    for link in links:

        r = requests.get(link)
        s = BeautifulSoup(r.content, 'html.parser')

        curr_ips = str(s).splitlines()
        if len(curr_ips) > 0:
            ips = ips + curr_ips
    
    print("Collected " + str(len(ips)) + " proxies from https://www.proxy-list.download/")

    return ips

# proxies scraped from https://spys.one/en/free-proxy-list/
def collect_5():

    print("Collecting proxies from https://spys.one/en/free-proxy-list/")

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
            proxy_anon = row[2].getText()

            if proxy_anon == "ANM":
                ips.append(row[0].getText())
    
    print("Collected " + str(len(ips)) + " proxies from https://spys.one/en/free-proxy-list/")

    return ips
    
# proxies scraped from https://www.socks-proxy.net/
def collect_6():
    print("Collecting proxies from https://www.socks-proxy.net/")

    r = requests.get("https://www.socks-proxy.net/")
    s = BeautifulSoup(r.content, 'html.parser')

    ip_table = s.find("table", {"class":"table table-striped table-bordered"})

    table_rows = list(ip_table.findChildren('tr'))
    
    # removes the head of the table
    table_rows.pop(0)

    ips = []

    for row in table_rows:
        
        cur_children = row.findChildren()

        proxy_anon = cur_children[4].getText()
        proxy_ip = cur_children[0].getText()
        proxy_port = cur_children[1].getText()

        if "transparent" not in proxy_anon:
            ips.append(proxy_ip + ":" + proxy_port)
    
    print("Collected " + str(len(ips)) + " proxies from https://www.socks-proxy.net/")

    return ips

# proxies scrapped from https://premiumproxy.net/elite-proxy-list
def collect_8():

    print("Collecting proxies from https://premiumproxy.net/elite-proxy-list")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    r = requests.get("https://premiumproxy.net/elite-proxy-list", headers = headers)
    s = BeautifulSoup(r.content, 'html.parser')

    ip_rows = s.find_all("tr", {"class":"pp1x"})
    ip_rows.pop(0)
    ip_rows.pop(0)

    for i in range(7):
        ip_rows.pop(len(ip_rows) - 1)

    ips = []

    for ip in ip_rows:
        ips.append(ip.findChildren()[0].getText())
    

    print("Collected " + str(len(ips)) + " proxies from https://premiumproxy.net/elite-proxy-list")

    return ips

# proxies scrapped from https://www.my-proxy.com/
def collect_10():

    print("Collecting proxies from https://www.my-proxy.com/")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    links = [
        "https://www.my-proxy.com/free-anonymous-proxy.html",
        "https://www.my-proxy.com/free-elite-proxy.html"
    ]


    ips = []
    for link in links:
        try:
            r = requests.get(link, headers = headers)
            s = BeautifulSoup(r.content, 'html.parser')

            table = s.find("div", {"class":"list"})

            ips = ips + table.getText(strip=True, separator='\n').splitlines()
        except:
            hi = 2

    print("Collected " + str(len(ips)) + " proxies from https://www.my-proxy.com/")

    return ips

# not working
def collect_9():

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    r = requests.get("https://premproxy.com/list/02.htm", headers = headers)
    s = BeautifulSoup(r.content, 'html.parser')

    ip_obj = s.find_all("td", {"data-label":"IP:port "})

    for ip in ip_obj:
        #print(s.find_all("span", {"class":"IP:port "}))
        print(ip.find('input')["value"])

        second_half = ip.find('input')["value"][ip.find('input')["value"].find("|"): len(ip.find('input')["value"])]
        print(ip.find("span", {"class":second_half}))

# not working
def collect_7():
    
    r = requests.get("https://www.proxynova.com/proxy-server-list/elite-proxies/")
    s = BeautifulSoup(r.content, 'html.parser')

    ip_table = s.find("table", {"class":"table"})

    children = ip_table.findChildren('tr')

    for child in children:
        print(child.findChildren()[0].getText())

# try each method
try:
    all_ips = all_ips + collect_1()
except Exception as e:
    print(e)
    print("Error: collect_1() failed")

try:
    all_ips = all_ips + collect_2()
except Exception as e:
    print(e)
    print("Error: collect_2() failed")

try:
    all_ips = all_ips + collect_3()
except Exception as e:
    print(e)
    print("Error: collect_3() failed")

try:
    all_ips = all_ips + collect_4()
except Exception as e:
    print(e)
    print("Error: collect_4() failed")

try:
    all_ips = all_ips + collect_5()
except Exception as e:
    print(e)
    print("Error: collect_5() failed")

try:
    all_ips = all_ips + collect_6()
except Exception as e:
    print(e)
    print("Error: collect_6() failed")

try:
    all_ips = all_ips + collect_8()
except Exception as e:
    print(e)
    print("Error: collect_8() failed")

try:
    all_ips = all_ips + collect_10()
except Exception as e:
    print(e)
    print("Error: collect_10() failed")

# convert list of all_ips to string
out = ""
for ip in all_ips:
    out = out + ip + "\n"
out = out[:len(out) - 1]

# write all the ips to untested_ips.txt
f = open(os.path.dirname(__file__) + "/untested_ips.txt", "w")
f.write(out)
f.close()