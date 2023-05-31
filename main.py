from proxy_generator import proxy_gen

# create the proxy generator object
obj = proxy_gen.proxy_gen()

# scrape the internet for proxies
obj.scrape()

# check the proxies that were previously collected and save the proxies to working_proxies.txt
obj.check()

# check the proxies that were previously collected and return the proxies as a list object
hi = obj.check_return()

print(hi)