from requests import get

class dhcp_client:
    def __init__(self, login_header=0, gateway="192.168.0.1", mac="xx-xx-xx-xx-xx-xx", ip="0.0.0.0", time=0):
        self.ip = ip
        self.mac = mac
        self.gateway = gateway
        self.time = time
        self.header = login_header

    def assignPermanentIp(self, permanent_ip):
        ip_assignment_url = 'http://{}/userRpm/FixMapCfgRpm.htm?Mac={}&Ip={}&State=1&Changed=0&SelIndex=0&Page=1&Save=Save'.format(
            self.gateway, self.mac, permanent_ip)
        get(ip_assignment_url, headers=self.header)
