#!/usr/bin/env python
# path06: testing influxdb 
# 
# current:
#   - getDBs - list available (preauth) databases
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



def getDBs():
  print OKGREEN + '  [+] path 6: influxdb - get DB\'s' + ENDC
  print ''

  # GET to IP:5601 to grab version
  print BOLD
  target = raw_input('    set target: ')
  print '    port: 8086'
  fullUrl = 'http://' + target + ':8086/query?q=SHOW+DATABASES&db=_internal'
  # print '    full url: ' + fullUrl # http://' + target + ':5601/app/kibana'

  print ENDC
  print '  [+] checking version...'
  req = requests.get(fullUrl)
  resp = req.text

  print BOLD
  print '   --- resp ---' + ENDC
  print resp
  print BOLD + '\n   --- end of resp --- \n' + ENDC


  print '' + BOLD
  print '  [+] path 06: influxdb - get DB\'s - finished.' + ENDC
  print ''


