from requests import get
from base64 import b64encode
from urllib.parse import quote
import re

class Instance(object):	
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
		
	def SystemReboot(self):
		get("http://192.168.0.1/userRpm/SysRebootRpm.htm?Reboot=Reboot", headers=self.auth)
	
	def resetStat(self):
		get("http://192.168.0.1/userRpm/SystemStatisticRpm.htm?DeleteAll=All", headers=self.auth)	
		
	def test(self, url):
		return get(url, headers=self.auth)
	
	def qoson(self):
		get("http://192.168.0.1/userRpm/QoSCfgSOHORpm.htm?QoSCtrl=1&h_lineType=1&h_down_bandWidth=4000&hips_1=100&hipe_1=120&hm_1=1&hbW_1=30&hn_1=&hen_1=1&hips_2=&hipe_2=&hm_2=0&hbW_2=&hn_2=&hen_2=&hips_3=&hipe_3=&hm_3=0&hbW_3=&hn_3=&hen_3=&hips_4=&hipe_4=&hm_4=0&hbW_4=&hn_4=&hen_4=&hips_5=&hipe_5=&hm_5=0&hbW_5=&hn_5=&hen_5=&hips_6=&hipe_6=&hm_6=0&hbW_6=&hn_6=&hen_6=&hips_7=&hipe_7=&hm_7=0&hbW_7=&hn_7=&hen_7=&hips_8=&hipe_8=&hm_8=0&hbW_8=&hn_8=&hen_8=&sv=Sav", headers=self.auth)
	
	def qosoff(self):
		get("http://192.168.0.1/userRpm/QoSCfgSOHORpm.htm?QoSCtrl=&h_lineType=0&h_down_bandWidth=2000&hips_1=&hipe_1=&hm_1=0&hbW_1=&hn_1=&hen_1=&hips_2=&hipe_2=&hm_2=0&hbW_2=&hn_2=&hen_2=&hips_3=&hipe_3=&hm_3=0&hbW_3=&hn_3=&hen_3=&hips_4=&hipe_4=&hm_4=0&hbW_4=&hn_4=&hen_4=&hips_5=&hipe_5=&hm_5=0&hbW_5=&hn_5=&hen_5=&hips_6=&hipe_6=&hm_6=0&hbW_6=&hn_6=&hen_6=&hips_7=&hipe_7=&hm_7=0&hbW_7=&hn_7=&hen_7=&hips_8=&hipe_8=&hm_8=0&hbW_8=&hn_8=&hen_8=&sv=Save", headers=self.auth)

	def GetChannel(self):
		return get("http://192.168.0.1/userRpm/WlanNetworkRpm.htm", headers=self.auth).text.split("\"Pulse\"")[1].split("\"TP-LINK_A95176_2\",")[0].split("\n")[7].split(",")[0]

	def reserveIp(self, mac, ip):
		get('http://{}/userRpm/FixMapCfgRpm.htm?Mac={}&Ip={}&State=1&Changed=0&SelIndex=0&Page=1&Save=Save'.format(self.gateway, mac, ip))
		self.SystemReboot()

	def SetChannel(self, ch):
		get("http://192.168.0.1/userRpm/WlanNetworkRpm.htm?ssid1=Pulse&ssid2=TP-LINK_A95176_2&ssid3=TP-LINK_A95176_3&ssid4=TP-LINK_A95176_4&region=101&channel={}&mode=5&chanWidth=2&ap=1&broadcast=2&brlssid=&brlbssid=&keytype=1&wepindex=1&authtype=1&keytext=&Save=Save".format(ch), headers=self.auth)
		self.SystemReboot()

	# def returnGET(self, url):
	# 	x = get(url, headers=self.auth)
	# 	return x
