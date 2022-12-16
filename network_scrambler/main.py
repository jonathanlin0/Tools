from applescript import tell
import os

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

for i in range(processes):

    tell.app( 'Terminal', 'do script "' + cmd + " " + str(iterations_per_window) + '"')