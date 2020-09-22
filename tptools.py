from requests import get
from base64 import b64encode
from urllib.parse import quote
from classes import dhcp_client
import re

class Instance:
	def __init__(self, gateway='192.168.0.1', username='admin', password='admin'):
		self.auth = dict()
		self.username = username
		self.password = password
		self.gateway = gateway
		self.url_stat = 'http://{}/userRpm/SystemStatisticRpm.htm'
		self.url_ip = 'http://{}/userRpm/AssignedIpAddrListRpm.htm'
		self.createheader(username, password, gateway)

	def createheader(self, user, password, gateway):
		auth_bytes = bytes(user+':'+password, 'utf-8')
		auth_b64_bytes = b64encode(auth_bytes)
		auth_b64_str = str(auth_b64_bytes, 'utf-8')
		auth_str = quote('Basic {}'.format(auth_b64_str))

		self.auth = {
		'Referer': 'http://'+gateway+'/', 
		'Authorization': auth_str,
		}
		
	def macresolver(self):
		resolve = dict()
		url = self.url_ip.format(self.gateway)
		r = get(url, headers=self.auth)
		ret = r.text.split("var DHCPDynList = new Array(")[1].split("0,0 );")[0].rstrip("\n")
		ret = re.finditer(".*[,]\n.*[,]\n.*[,]\n.*[,]", ret)
		for item in ret:
			new = item.group(0).split(",\n")
			resolve[new[1]] = new[0]
		return resolve
		
	def ipresolver(self):
		resolve = dict()
		url = self.url_ip.format(self.gateway)
		r = get(url, headers=self.auth)
		ret = r.text.split("var DHCPDynList = new Array(")[1].split("0,0 );")[0].rstrip("\n")
		ret = re.finditer(".*[,]\n.*[,]\n.*[,]\n.*[,]", ret)
		for item in ret:
			new = item.group(0).split(",\n")
			resolve[new[2]] = new[0]
		return resolve
		
	def stat(self):
		stat = []
		r = get("http://192.168.0.1/userRpm/SystemStatisticRpm.htm?sortType=5", headers=self.auth).text.split("var statList = new Array(\n")[1].split("0,0 );")[0].split("\n")
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

	def returnGET(self, url='http://192.168.0.1/userRpm/AssignedIpAddrListRpm.htm'):
		x = get(url, headers=self.auth)
		return x

	def test(self, mac='D0-53-49-11-EB-75', ip='192.168.0.1', permip='192.168.0.100'):
		x = dhcp_client(self.auth, self.gateway, mac, ip)
		x.assignPermanentIp(permip)