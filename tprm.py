from requests import get
from base64 import b64encode
from urllib.parse import quote
from time import sleep
from hurry.filesize import size
import os
import re

tplink = '192.168.0.1'
user = 'admin'
password = 'admin'
url_stat = 'http://{}/userRpm/SystemStatisticRpm.htm'
url_ip = 'http://{}/userRpm/AssignedIpAddrListRpm.htm'

def SaveToFile(text, filename):
	file = open(filename, "w")
	file.write(text)

auth_bytes = bytes(user+':'+password, 'utf-8')
auth_b64_bytes = b64encode(auth_bytes)
auth_b64_str = str(auth_b64_bytes, 'utf-8')

auth_str = quote('Basic {}'.format(auth_b64_str))

auth = {
'Referer': 'http://'+tplink+'/', 
'Authorization': auth_str,
}

resolve = dict()

url = url_ip.format(tplink)
r = get(url, headers=auth)
ret = r.text.split("var DHCPDynList = new Array(")[1].split("0,0 );")[0].rstrip("\n")
ret = re.finditer(".*[,]\n.*[,]\n.*[,]\n.*[,]", ret)
for item in ret:
	new = item.group(0).split(",\n")
	resolve[new[1]] = new[0]
	
get("http://192.168.0.1/userRpm/SystemStatisticRpm.htm?DeleteAll=All", headers=auth)

while True:
	os.system('cls')
	url = url_stat.format(tplink)
	r = get("http://192.168.0.1/userRpm/SystemStatisticRpm.htm", headers=auth).text.split("var statList = new Array(\n")[1].split("0,0 );")[0].split("\n")
	for line in r:
		if line != "":
			line = line.split(",")
			print(line[1] + " " + resolve[line[2]] + " " + line[4] + " " + line[6])
	sleep(1)