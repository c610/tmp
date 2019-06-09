#!/usr/bin/env python
# path08: testing pcp 
# 
# current:
#   - getstats
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



def getstats():
  # Available Commands:     atop atopsar collectl dmcache dstat
  #  free iostat ipcs lvmcache mpstat numastat pidstat python
  #  shping summary tapestat uptime verify vmstat

  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('    set port: ')

  try:
    print '\n  --- response ---\n'
    cmd = 'uptime'
    pcp = 'pcp -h ' + target + ' -p ' + port + ' ' + cmd    
    subprocess.call([ pcp ], shell=True)

    print '\n  --- response ---\n'
  except:
    print FAIL + '  [-] Can not find pcp - install it!\n' + ENDC
  

  print OKGREEN + '  [+] path 8: testing pcp' + ENDC
  print ''
  

  print '' + BOLD
  print '  [+] path 08: testing pcp - finished.' + ENDC
  print ''

