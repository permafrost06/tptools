from requests import get
from time import sleep
from hurry.filesize import size
from helpers import auth, macresolve, ipresolve, resetStat, stat
import os

# variables for username, password, and gateway/referer
tplink = '192.168.0.1'
user = 'admin'
password = 'admin'

# check otherusers.py if above three variables are different and require input

# variables for "Statistics" and "DHCP Clients List" pages' addresses
url_stat = 'http://{}/userRpm/SystemStatisticRpm.htm'
url_ip = 'http://{}/userRpm/AssignedIpAddrListRpm.htm'

# create authentication header
auth = auth(user, password, tplink)

# prepares "DHCP Clients List" url to create MAC resolver
url = url_ip.format(tplink)

resolve = ipresolve(url, auth)

# delete current statistics data

resetStat(auth)

# run inifnitely
while True:
	os.system('cls')
	# prepares "Statistics" url for fetching speed data
	url = url_stat.format(tplink)
	
	# splits the data until only the required ones remain
	r = stat(auth)
	for item in r:
		print(item["mac"] + " " + resolve[item["ip"]] + " " + item["bytes_total"] + " " + item["bytes_curr"])
	# delay
	sleep(1)