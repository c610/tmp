#!/usr/bin/env python
# path05: testing splunk
# 
# current:
#   - getversion
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



def getversion():
  print OKGREEN + '  [+] path 5a: Splunk webapp (default:8000/tcp)' + ENDC
  print ''

  # GET to IP:5601 to grab version
  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('  set port: ')
  print ENDC

  print OKBLUE
  print '  [+] Trying to identify version...' + ENDC 

  fullUrl = 'http://' + target + ':' + port + '/en-US/'
  req = requests.get(fullUrl)
  resp = req.text

  find = re.compile('<p class="footer">&copy; (.*?).</p>')
  found = re.search(find, resp)

  if found:
    print OKGREEN
    print '  [+] Found version: ' + found.group(1) + '\n' + ENDC

  #
  print '' + BOLD
  print '  [+] path 05a: Splunk webappp - finished.\n' + ENDC
  print ''

##


def getrest():
  print OKGREEN + '  [+] path 5b: Splunk REST API (default: 8089/tcp)' + ENDC
  print ''

  # GET to IP:5601 to grab version
  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('  set port: ')
  print ENDC

  print OKBLUE
  print '  [+] Trying to identify version...' + ENDC

  # grabbed from: 
  # https://stackoverflow.com/questions/47716695/write-log-entry-to-splunk-via-http-in-python/47756716#47756716
  url='https://' + target + ':8089/'
  authHeader = {'Authorization': 'Splunk {}'.format('ABCDEFG-8A55-4ABB-HIJK-1A7E6637LMNO')}
  jsonDict = {"index":"cloud_custodian", "event": { 'message' : "Sample pentest message" } }

  r = requests.post(url, headers=authHeader, json=jsonDict, verify=False)
  resp = r.text

  find_title = re.findall("<title>(.*?)</title>", resp, re.MULTILINE)
  #find_ids = re.findall("<id>(.*?)</id>", resp, re.MULTILINE)

  for title in find_title:
    print OKGREEN
    print '  Found title: %s' % ( title ) 
    print ENDC + BOLD 
    # req2: GETi found services
    try:
      getservice = 'https://' + target + ':' + port+ '/' + title
      req2 = requests.get(getservice, headers=authHeader, verify=False)
      resp2 = req2.text
      find_links = re.findall('<link href="(.*?)" rel=', resp2, re.MULTILINE)


      print '    Links:\n' + ENDC
      for link in find_links:
        print '     link -> %s' % ( link ) 

      print '    --- end of service %s ---\n' % ( title )



    except requests.exceptions.ConnectionError as e:
      print '    [-] error when requesting %s:\n%s' % ( title, e )
      pass

 


  #
  print '' + BOLD
  print '  [+] path 05b: Splunk webappp - finished.\n' + ENDC
  print ''

##

