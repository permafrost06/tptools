from bs4 import BeautifulSoup
from requests import get
from base64 import b64encode
from urllib.parse import quote

user = 'admin'
password = 'admin'
gateway = '192.168.0.1'

auth_bytes = bytes(user+':'+password, 'utf-8')
auth_b64_bytes = b64encode(auth_bytes)
auth_b64_str = str(auth_b64_bytes, 'utf-8')
auth_str = quote('Basic {}'.format(auth_b64_str))

auth = {
'Referer': 'http://'+gateway+'/', 
'Authorization': auth_str,
}

x = BeautifulSoup(get('http://{}/userRpm/SystemStatisticRpm.htm'.format(gateway), headers=auth).text)