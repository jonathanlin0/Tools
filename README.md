A collection of tools. The following code is for educational purposes ONLY. Do not use the following code for malicious purposes.

Due to my limited funding as a college student, I only have a Macbook. Therefore, some of the programs in this repository only work on MacOS, but most of my code uses common packages, so it shouldn't be too hard to change a few settings in the code for it to work on Windows and/or Linux.

### How To Use

Please use pip or pip3 to install all the packages in `requirements.txt`. Afterwards, please open terminal and navigate to the root folder. The root folder is this current folder, not the project specific folders. The running instructions for each project listed below are from this directory, NOT the project specific directory.

### Disclaimers

For the purposes of increasing performance, many of the programs in this repository utilizes parallel computing. As a result, many of the programs gives you an option to set how many "threads" you would like. A thread refers to an instance of the program. For example, if you set it as 15 threads for a program, 15 copies of the selected script will run simultaneously. Here are my recommendations for thread count when running my programs:

50 - low-end laptop

150 - decent laptop

250+ - high-end computer

## form_filler

### Function
This program can automatically fill out Google Forms for you.

### Usage:
`python3 form_filler/main.py`

Please ensure your chromedriver in `form_filler/chromedriver` is up-to-date. To download the latest chromedriver, visit [here](https://chromedriver.chromium.org/downloads). For more information on chromedriver, please visit [here](https://chromedriver.chromium.org/).

Note: chromedriver is utilized for initial data form collection. The program uses Requests to fill out Google Forms, not Selenium or any other form of browser testing.

## network_scrambler

### Function
This program sends random requests.

### Usage:
`python3 network_scrambler/main.py`

## proxy_generator

### Function
This program searches the internet for proxies. After collecting a few thousand proxies, it then uses the proxies to ping Google (with a timeout of 1 second) to check them.

### Usage:

Ensure that the proxy\_generator folder is in the same directory as the file(s) that you want to use the proxy\_generator package

```python
from proxy_generator import proxy_gen

# create the proxy generator object
obj = proxy_gen.proxy_gen()

# scrape the internet for proxies
obj.scrape()

# check the proxies that were previously collected
obj.check()
```