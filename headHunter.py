#!/usr/bin/env python
# headHunter.py - small script to check few headers for
# buggy server configuration.
# @22.10.2016
# based on 'python web penetration testing cookbook'
#
import requests
import sys

GREEN = '\033[92m'
YELLOW = '\033[93m'
ENDC = '\033[0m'
RED = '\033[31m'

target = str(sys.argv[1])
print '\n\t    ( headHunter.py - find buggy headers )\n'

print '[+] Checking : ' + GREEN + target + ENDC + '\n'

req = requests.get(target)

try:
  xssprotect = req.headers['X-XSS-Protection']
  if xssprotect != '1; mode=block':
    print RED + '  [bug] X-XSS-Protection not set properly, XSS may be possible: ' + xssprotect + ENDC
except:
  print RED + '  [bug] X-XSS-Protection not set, XSS may be possible' + ENDC

try:
  contenttype = req.headers['X-Content-Type-Options']
  if contenttype != 'nosniff':
    print RED+ '  [bug] X-Content-Type-Options not set properly: ' + contenttype + ENDC
except:
  print RED + '  [bug] X-Content-Type-Options not set' + ENDC

try:
  hsts = req.headers['Strict-Transport-Security']
except:
  print RED + '  [bug] HSTS header not set, MITM attacks may be possible' + ENDC

try:
  csp = req.headers['Content-Security-Policy']
  print YELLOW + '  [info] Content-Security-Policy set:'+csp + ENDC
except:
  print RED + '  [bug] Content-Security-Policy missing' + ENDC

try:
  srv = req.headers['Server']
  print YELLOW + '  [info] Server set:' + srv + ENDC
except:
  print YELLOW + '  [info] Server header not found' + ENDC

try:
  dat = req.headers['Date']
  print YELLOW + '  [info] Date set: ' +  dat + ENDC
except:
  pass

try:
  crossdomain = req.headers['Access-Control-Allow-Origin'] # if set to '*' = bug
  print YELLOW+'  [info] Access-Control-Allow-Origin set:' + crossdomain + ENDC
except:
  print YELLOW+'  [info] Access-Control-Allow-Origin missing' + ENDC

try:
  xcsp = req.headers['X-Content-Security-Policy']
  print YELLOW+'  [info] X-Content-Security-Policy set:'+ xcsp + ENDC
  # specify per-document, the ability to perform actions
  # that would normally be permitted under SOP.
except:
  print YELLOW+'  [info] X-Content-Security-Policy missing' + ENDC

try:
  print YELLOW+'  [info] X-Frame-Options presented, clickjacking not likely possible' + ENDC
except:
  print RED + '  [bug] X-Frame-Options missing - clickjacking possible' + ENDC


# TODO: add more headers...
print '\n[+] Test finished.\n'


