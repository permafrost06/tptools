from time import sleep
from tptools import Instance
import os
from helper import get_

x = Instance("192.168.0.1", "admin", "admin")

resolve = x.ipresolver()

x.resetStat()

# run inifnitely
while True:
	os.system('cls')
	# splits the data until only the required ones remain
	r = x.stat()
	for item in r:
		print(item["mac"] + " " + resolve[item["ip"]] + " " + get_(int(item["bytes_curr"]))+"ps")
	# delay
	sleep(1)