#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# core.py - main function(s) for our starter...
#
# - 26.05.2019 @ 10:56
#
# detailed tutorial:
#  https://www.youtube.com/watch?v=S1j4K_D3ZQo
#

# --- imports ---
import sys
sys.path.append('files')
import datetime
import os
import subprocess
#from pymongo import MongoClient
from stomp import * # for STOMP protocol
import stomp


# --- paths/implants ---
import path01      # openssh enum bug
import path02      # kibana getversion
import path03      # testing elasticsearch
import path04      # testing oracle tns listener
import path05      # testing splunk
import path06      # testing influxdb
import path07      # testing mongodb
import path08      # testing pcp
import path09      # testing mysql
import path10      # testing prometheus # (still todo)
import path11      # testing active mq web console (8191) / stomp
import path12      # testing vamax 8.x rce
import path13      # testing activemq - admin panel
import path14      # testing JWDP protocol

import implants
# ...wanna more?

# --- defines ---
now = datetime.datetime.now()
current_date = now.strftime("%d.%m.%Y %H:%M")

# --- super colours ---
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'



## --- functions ---
def banner():
  #      *****************************************************************
  print WARNING + '\n'
  print ' ███████╗███╗   ██╗██╗     ██╗██╗   (' + str(current_date) + ')'
  print ' ██╔════╝████╗  ██║██║     ██║██║      '
  print ' █████╗  ██╔██╗ ██║██║     ██║██║      '
  print ' ██╔══╝  ██║╚██╗██║██║     ██║██║      '
  print ' ███████╗██║ ╚████║███████╗██║███████╗ '
  print ' ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝╚══════╝ '
  print ENDC


  #print '*'*65
  #print '   *** enlil - v0.1 ***                     (' + str(current_date) +')'
  #print '*'*65 + ENDC + '\n'

##

def menu():
  print OKBLUE + '  Ask me for:' + ENDC
  print '    ' + UNDERLINE + '1] scan' + ENDC
  print '    ' + UNDERLINE + '2] readlog' + ENDC
  print '    ' + UNDERLINE + '3] path'  + ENDC
  print '    ' + UNDERLINE + '4] implant' + ENDC
  print ''
  choice = raw_input('  > ')
  print ''

  if choice == '1':    # 1] scan
    print OKGREEN + '  [+] your choice: ' + choice + ENDC
    print '  [+] preparing scan...'
    scan_target()
    menu()

  elif choice == '2':  # 2] readlog
    print OKGREEN + '  [+] your choice: ' + choice + ENDC
    readlog_target()
    menu()

  elif choice == '3':  # 3] path
    print OKGREEN + '  [+] your choice: ' + choice + ENDC
    path_target()
    menu()

  elif choice == '4':  # 4] implant
    print OKGREEN + '  [+] your choice: ' + choice + ENDC
    implants.run()
    menu()

  elif choice == 'q':
    print FAIL + '  \n  Well... bye :7\n' + ENDC
    sys.exit(0)

  else:
    print BOLD + '  [-] wrong, again Neo\n' + ENDC
    menu()


##

def scan_target():
  # run scan now, when all env is ready to future  log/s
  print OKBLUE
  target = raw_input('  target[IP]> ')
  print ENDC

  # check/prepare env (if needed)
  prepare_env(target)

  # run the scan when all settings/env are ready
  cmd = 'nmap -sV -vvv -n --top-ports 15000 -Pn --max-retries 1 --min-rate 120 -oN ' + './' + target + '/' + target + '.log ' + target
  # cmd = 'nmap -sV -v -n -p- -Pn --max-retries 1 --min-rate 121 -oN ' + './' + target + '/'+ target + '.log ' + target
  runme = subprocess.call([ cmd ], shell=True)

  print '\n'
  print OKGREEN + '  [i] Scan module finished.\n' + ENDC

##

def prepare_env(target):
  print BOLD + '  [i] checking env for target: ' + target + ENDC

  pwd = os.getcwd()
  print OKGREEN + '  [+] pwd: ' + pwd + ENDC

  # checking for target logdir
  targetLogDir = pwd + '/' + target
  if os.path.exists(targetLogDir):
   print OKGREEN + '  [+] Target logdir exists, skip' + ENDC
  else:
   # create log dirs
   try:
     os.mkdir(targetLogDir)
     print OKGREEN + '  [+] Log directory created : ' + targetLogDir + ENDC
   except OSError, e:
     print OKGREEN + '  [+] Log directory is already there' + ENDC

  print '\n'

##

def readlog_target():
  pwd = os.getcwd()

  # first of all: check for target's env
  print OKBLUE
  read_target = raw_input('  > Read target[IP]> ')
  print ENDC

  # checking for env for our target; must be scanned first of log
  # should be placed 'manually'
  prepare_env(read_target)

  print '\n'
  print '------------------------------------------------'
  print BOLD + '  [i] Found open port(s):' + ENDC
  print '------------------------------------------------'
  # find open ports now
  targetLogFile = pwd + '/' + read_target + '/' + read_target + '.log'
  fp = open(targetLogFile, 'r')
  lines = fp.readlines()

  for line in lines:
    if line.find('/tcp') != -1:
      if line.find('open') != -1:
        print '        [open port]: ' + line.rstrip()


  print '\n'

##

def path_target():
  pwd = os.getcwd()

  print OKBLUE
  # readl log for specific target and prepare some useful path(s)
  target = raw_input('  target[IP]> ')
  print ENDC

  # prepare_env(target) # if needed
  print '\n'
  print BOLD + '  [i] Found possible path(s):' + ENDC
  targetLogFile = pwd + '/' + target + '/' + target + '.log'


  fp = open(targetLogFile, 'r')
  lines = fp.readlines()

  path_num = 0
  print HEADER
  for line in lines:
    if line.find('OpenSSH') != -1:
      substring = "OpenSSH"
      string = line # ex. "Banner 22/tcp         OpenSSH 7.7p321"
      substring_list = ['OpenSSH 5.','OpenSSH 6.','OpenSSH 7.7','OpenSSH 7.']
      vulnerable = any(substring in string for substring in substring_list)
      #print vulnerable

      if vulnerable == True:
        print '  [path 01]> possibly openssh user enum bug'
        # run pocssh now

    elif line.find('5601/tcp') != -1:
      print '  [path 02]> kibana webapp'

    elif line.find('9200/tcp') != -1:
      print '  [path 03a]> ElasticSearch at 9200 - check version'

    elif line.find('9200/tcp') != -1:
      print '  [path 03b]> ElasticSearch at 9200 - preauth search'

    elif line.find('Oracle TNS listener') != -1:
      if line.find('unauthorized') != -1:
        print '  [path 04] Oracle TNS listener found'

    elif line.find('8000/tcp') != -1:
      if line.find('CherryPy httpd') != -1:
        print '  [path 05a] Splunk get version (default: 8000/tcp)'

    elif line.find('8089/tcp') != -1:
      print '  [path 05b] Splunk REST API check (default: 8089/tcp)'

    elif line.find('InfluxDB') != -1:
      print '  [path 06] InfluxDB - preauth get DB\'s'

    elif line.find('8086/tcp') != -1:
      print '  [path 06] InfluxDB - preauth get DB\'s'

    elif line.find('MongoDB') != -1:
      print '  [path 07a] MongoDB found' # run# apt-get install python-pymongo
      print '  [path 07b] MongoDB - postauth list '

    elif line.find('44321/tcp') != -1:
      print '  [path 08] PCP found online' # run# apt-get install pcp-manager

    elif line.find('MySQL') != -1:
      if line.find('unauthorized') != -1:
        print '  [path 09] MySQL found unauthorized'

    elif line.find('Go-IPFS json-rpc or InfluxDB API') != -1:
      if line.find('9090/tcp') != -1: # default for Prometheus
        print '  [path 10] Go-IPFS json-rpc/InfluxDB API/Prometheus - found'

    elif line.find('8161/tcp') != -1:
      print '  [path 11] Active MQ - Web Console found'

    elif line.find('9080/tcp') != -1:
      print '  [path 12] VA MAX (8.3.x) - possible RCE'

    elif line.find('61616') != -1: # 61613-6/tcp
      print '  [path 13] ActiveMQ STOMP found'

    elif line.find('5005') != -1: # default jwdp
      print '  [path 14] JWDP service found open'
    elif line.find('JWDP') != -1: # TODO: ;]
      print '  [path 14] JWDP service found open'


    # next...

  print ENDC # of HEADER for path(s)
  print OKGREEN + '  [+] searching for path(s) - finished.\n' + ENDC

  print BOLD
  try_path = raw_input('  [?] Path to try> ')
  print ENDC

  if try_path == '1'    : path01.enum()           # path01: ssh enum bug
  elif try_path == '2'  : path02.getversion()     # path02: kibana webapp
  elif try_path == '3a' : path03.getversion()     # path03a: elasticsearch on 9200
  elif try_path == '3b' : path03.preauth_search() # path03b: elasticsearch preauth search
  elif try_path == '4'  : path04.tnscmds()        # path04: preauth tns listener, ver, stat
  elif try_path == '5a' : path05.getversion()     # path05a: testing splunk at 8000/tcp
  elif try_path == '5b' : path05.getrest()        # path05b: testing splunk at 8089/tcp
  elif try_path == '6'  : path06.getDBs()         # path06: influxdb - get databases
  elif try_path == '7a' : path07.preauthlist()    # path07: preauth list available DB's
  elif try_path == '7b' : path07.postauthlist()   # path07: postauth list available DB's
  elif try_path == '8'  : path08.getstats()       # path08: pcp stats online
  elif try_path == '9'  : path09.getdbs()     # path09: testing mysql
  # elif try_path == '10' : path10.getinfo()        # path10: prometheus - getinfo
  elif try_path == '11' : path11.getadminlogin()  # path11: active mq web console small bf test
  elif try_path == '12' : path12.getrce()         # path12: vamax 8.3.x rce
  elif try_path == '13a': path13.bf()             # admin panel bf activemq
  elif try_path == '13b': path13.sender()         # stomp sender activemq
  elif try_path == '14' : path14.gotleak()        # path14: testing jdwp

  # ...
  else:
    print FAIL + '  Don\'t play with me.\n' + ENDC


  print '\n'
  menu() # # goto 'main' starter: menu()

##
