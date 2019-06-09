#!/usr/bin/env python
# path10: testing Prometheus (9090/tcp)
# 
# current:
#   - (preauth) getinfo
#  

# --- imports ---
import subprocess
import re
import requests
import sys
import urllib3
urllib3.disable_warnings()

# --- super colours ---
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'



def getinfo():
  print OKGREEN + '  [+] path 10: Prometheus - pretuah - get_info' + ENDC
  print ''

  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('  set port: ') # default 9090/tcp
  print ENDC

  print OKBLUE
  print '  [+] Trying to identify version...' + ENDC 

  # ... STILL IN PROGRESS... ;Z ...


  #
  print '' + BOLD
  print '  [+] path 10: Prometheus - preauth - get_info - finished.\n' + ENDC
  print ''

##



