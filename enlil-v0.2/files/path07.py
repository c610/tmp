#!/usr/bin/env python
# path07: testing mongodb
# 
# note: to use this path you'll need to:
#    # apt-get install python-pymongo -y
# 
# current:
#   - preauthlist
#   - postauthlist 

# --- imports ---
import pymongo
from pymongo import MongoClient
import subprocess
import re

# --- super colours ---
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def preauthlist():
  print OKGREEN + '  [+] path 7a: mongodb - preauth list DB\'s' + ENDC

  # GET to IP:5601 to grab version
  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('    set port[27017]: ')

  try:
    client = MongoClient(target, int(port) )
    print OKGREEN + '\n  [+] We are connected! :)\n' + ENDC
    print BOLD + '  [+] Listing available databases:' + ENDC
    dbs = client.list_database_names()
    for db in dbs:
      print '    -db-> %s' % ( db ) 

  except pymongo.errors.OperationFailure:
    print FAIL + '  [-] We need some credentials to access DB ;[\n' + ENDC

  except pymongo.errors.ServerSelectionTimeoutError:
    print FAIL + '  [-] We can not connect to remote DB (timeout) :Z\n' + ENDC


  print '' + BOLD
  print '  [+] path 7a: mongodb - preauth list - finished.' + ENDC
  print ''

def postauthlist():
  print OKGREEN + '  [+] path 7b: mongodb - postauth list DB\'s' + ENDC

  # GET to IP:5601 to grab version
  print BOLD
  target = raw_input('    set target: ')
  port = raw_input('    set port[27017]: ')
  user = raw_input('    try username: ')
  passwd = raw_input('    try password: ')

  conn_str = 'mongodb://' + user + ':' + passwd + '@' + target + ':' + port + '/'
  # print conn_str

  try:
    client = MongoClient( conn_str )
    print OKGREEN + '\n  [+] We are connected! :)\n' + ENDC
    print BOLD + '  [+] Listing available databases:' + ENDC
    dbs = client.list_database_names()
    for db in dbs:
      print '    -db-> %s' % ( db )

  except pymongo.errors.OperationFailure:
    print FAIL + '  [-] Wrong credentials :C\n' + ENDC

  except pymongo.errors.ServerSelectionTimeoutError:
    print FAIL + '  [-] We can not connect to remote DB (timeout) :Z\n' + ENDC


  print '' + BOLD
  print '  [+] path 7b: mongodb - postauth list - finished.' + ENDC
  print ''



