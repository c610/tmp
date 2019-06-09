#!/usr/bin/env python
# path02: testing kibana
# 
# current:
#   - getversion 
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



def getversion():
  print OKGREEN + '  [+] path 2: kibana webapp' + ENDC
  print ''

  # GET to IP:5601 to grab version
  print BOLD
  target = raw_input('    set target: ')
  print '    port: 5601'
  fullUrl = 'http://' + target + ':5601/app/kibana'
  print '    full url: ' + fullUrl # http://' + target + ':5601/app/kibana'

  print ENDC
  print '  [+] checking version...'
  req = requests.get(fullUrl)
  resp = req.text

  findver = re.compile('kbn-injected-metadata data="{&quot;version&quot;:&quot;(.*?)&quot;,')
  foundver = re.search(findver, resp)

  if foundver:
    print OKGREEN
    print '  [+] Kibana version: %s' % ( foundver.group(1) )
    print ENDC

  else:
    print FAIL + '  [-] Could not determine Kibana version, sorry :<' + ENDC
    print ''


  print '' + BOLD
  print '  [+] path 02: kibana webappp - finished.' + ENDC
  print ''


