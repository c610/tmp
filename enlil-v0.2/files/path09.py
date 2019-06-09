#!/usr/bin/env python
# path09: finding mysql
# 
# current:
#   - ...
#  

# --- imports ---
import subprocess
import re
import MySQLdb

# --- super colours ---
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def getdbs():
  print OKGREEN + '  [+] path 9: testing mysql' + ENDC
  print ''

  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('    set port: ')

  try:
    # connecting people 
    db = MySQLdb.connect( host = target,
                          user='mysql',
                          passwd='',
                          db='' )

    # creating cursor for all execs/queries
    cur = db.cursor()

    # gogogo
    cur.execute("show databases")

    for row in cur.fetchall():
      print row[0]

    db.close()

  except MySQLdb.OperationalError:
    print FAIL + '\n    [-] Can not connect, sorry :Z\n' + ENDC



  print '' + BOLD
  print '  [+] path 9: testing mysql  - finished.' + ENDC
  print ''


