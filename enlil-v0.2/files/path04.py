#!/usr/bin/env python
# path04: oracle tns listener
# 
# current:
#   -- tnscmd10g using: ping, status, version
# 

# --- imports ---
import subprocess
import re

# --- super colours ---
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'



def tnscmds():
  print OKGREEN + '  [+] path 4: oracle tns listener unauthorized' + ENDC
  print '' + BOLD

  target = raw_input('  set target: ')
  port = raw_input('  set port: ')
  print ENDC

  # try ping
  print OKGREEN
  print '\n  [+] checking: ping\n' + ENDC
  check_ping = 'tnscmd10g ping -h ' + target + ' -p ' + port
  subprocess.call([check_ping], shell=True)
  print '\n'

  print OKGREEN + '  [+] checking: version\n' + ENDC
  check_vers = 'tnscmd10g version -h ' + target + ' -p ' + port
  subprocess.call([check_vers], shell=True)
  print '\n'

  print OKGREEN + '  [+] checking: status\n' + ENDC
  check_stat = 'tnscmd10g status -h ' + target + ' -p ' + port
  subprocess.call([check_stat], shell=True)
  print '\n'


  print OKGREEN
  print '  [+] path 4: oracle tns listener - finished.\n' + ENDC

## 
