#!/usr/bin/python3

import requests
import re
import ipaddress

class HwSwitch:
    """Configuration of power switch must be done via browser.
    Configuration page is written in Adobe Flash technology.
    Default values:
    - pulse duration - 10 seconds
    - slaves status - ON
    - user - admin
    - password - admin
    - n - outlet number of switch
    - func - on, off, pulse, toggle
    - ?s=0 - show status

    docs http://www.produktinfo.conrad.com/datenblaetter/975000-999999/999171-an-01-ml-Kurzanl_INFRATEC_IP_PM211_MIP_de_en_es.pdf
    """


    def __init__(self, ip, user="admin", passwd="admin"):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.status_string = "?s=0"
        self.status = [True, True]
    
    def send_request(self, params):
        return requests.get('http://' + self.ip + '/sw', params=params)

    def get_status(self):
        params = {'s':'0'}
        r = self.send_request(params)
        return self.parse_status(r.text)

    def o_status(self, outlet: int) -> bool:
        return self.status[outlet-1]

    def _set_status(self):
        status = self.get_status()
        if status['1'] == '1':
            self.status[0] = True
        elif status['1'] == '0':
            self.status[0] = False

        if status['2'] == '1':
            self.status[1] = True
        elif status['2'] == '0':
            self.status[1] = False
        
    def parse_status(self, body):
        m = re.findall(r'Out\s(\d):\s(\d)', body)
        return dict( (x,y) for x, y in m)

    def on(self, outlet: int):
        params = {'u':self.user, 'p':self.passwd, 'o':outlet, 'f':'on'}
        r = self.send_request(params)
        return self.parse_status(r.text)

    def off(self, outlet: int):
        params = {'u':self.user, 'p':self.passwd, 'o':outlet, 'f':'off'}
        r = self.send_request(params)
        return self.parse_status(r.text)

    def pulse(self, outlet: int):
        params = {'u':self.user, 'p':self.passwd, 'o':outlet, 'f':'pulse'}
        r = self.send_request(params)
        return self.parse_status(r.text)

    def toggle(self, outlet: int):
        params = {'u':self.user, 'p':self.passwd, 'o':outlet, 'f':'toggle'}
        r = self.send_request(params)
        return self.parse_status(r.text)


pc = HwSwitch('192.168.0.211')
s = pc.off(2)
print(s)
print(pc.o_status(2))