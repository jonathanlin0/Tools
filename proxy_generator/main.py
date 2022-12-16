from applescript import tell
import os

windows = 50

f = open(os.path.dirname(__file__) + "/untested_ips.txt")
all_ips = f.read().splitlines()
f.close()

total_length = len(all_ips)

# truncate the remainder ips
ips_per_window = int(total_length / windows)

cmd = "python3 " + os.path.dirname(__file__) + "/checker.py"

for i in range(windows):

    starting_index = i + 1
    starting_index = starting_index * ips_per_window

    tell.app( 'Terminal', 'do script "' + cmd + " " + str(starting_index) + " " + str(ips_per_window) + '"')