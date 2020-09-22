from requests import get
from base64 import b64encode
from urllib.parse import quote
import re

def auth(user, password, tplink):
	auth_bytes = bytes(user+':'+password, 'utf-8')
	auth_b64_bytes = b64encode(auth_bytes)
	auth_b64_str = str(auth_b64_bytes, 'utf-8')

	auth_str = quote('Basic {}'.format(auth_b64_str))

	return {
	'Referer': 'http://'+tplink+'/', 
	'Authorization': auth_str,
	}
	
def macresolve(url, auth):
	resolve = dict()
	r = get(url, headers=auth)
	ret = r.text.split("var DHCPDynList = new Array(")[1].split("0,0 );")[0].rstrip("\n")
	ret = re.finditer(".*[,]\n.*[,]\n.*[,]\n.*[,]", ret)
	for item in ret:
		new = item.group(0).split(",\n")
		resolve[new[1]] = new[0]
	return resolve
	
def ipresolve(url, auth):
	resolve = dict()
	r = get(url, headers=auth)
	ret = r.text.split("var DHCPDynList = new Array(")[1].split("0,0 );")[0].rstrip("\n")
	ret = re.finditer(".*[,]\n.*[,]\n.*[,]\n.*[,]", ret)
	for item in ret:
		new = item.group(0).split(",\n")
		resolve[new[2]] = new[0]
	return resolve
	
def stat(auth):
	stat = []
	r = get("http://192.168.0.1/userRpm/SystemStatisticRpm.htm?sortType=5", headers=auth).text.split("var statList = new Array(\n")[1].split("0,0 );")[0].split("\n")
	for line in r:
		if line != "":
			line = line.split(",")
			stat.append({
			'ip': line[1],
			'mac': line[2],
			'pact_total': line[3],
			'bytes_total': line[4],
			'pact_curr': line[5],
			'bytes_curr': line[6]
			})
	return stat
	
def resetStat(auth):
	get("http://192.168.0.1/userRpm/SystemStatisticRpm.htm?DeleteAll=All", headers=auth)