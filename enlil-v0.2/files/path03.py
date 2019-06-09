#!/usr/bin/env python
# path03: elasticsearch 
# 
# current:
#   - getversion
#   - preauth_search
# 

# --- imports ---
import subprocess
import requests
import json

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
  print OKGREEN + '  [+] path 3a: elasticsearch on 9200 - get version' + ENDC
  print

  print BOLD
  target = raw_input('  set target: ')
  print '    port: 9200' + ENDC

  fullUrl = 'http://' + target + ':9200/'
  headers = {'content-type':'application/json'}

  print OKBLUE + '  [i] checking version...' + ENDC
  req = requests.get(fullUrl, headers=headers)
  resp = req.text

  print '  -- resp --\n'
  print resp
  print '  -- end of resp --\n'

  print BOLD + '  [+] path 3a - elasticsearch on 9200 - get version - finished.\n' + ENDC

## 


def preauth_search():
  print OKGREEN + '  [+] path 3b: elasticsearch on 9200 - preauth search' + ENDC
  print ''

  print BOLD
  target = raw_input('    set target: ')
  print '    port: 9200'
  print ENDC

  fullUrl = 'http://' + target + ':9200/_search'
  url_data = {"query":{"match_all":{}}}
  headers = {'content-type':'application/json'}

  print OKBLUE + '  [i] sending search request...' + ENDC
  req = requests.post(fullUrl, data=json.dumps(url_data), headers=headers)
  resp = req.text

  print '  -- resp --\n'
  print resp
  print ' -- end of resp --\n'

  print BOLD + '  [+] path 3b - elasticsearch on 9200 - preauth search - finished.\n' + ENDC

## 


