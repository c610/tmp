#!/usr/bin/env python
# ---------------------------------------------------------------
# code16.py - small wrapper for OpenVAS
# 26.12.2016 17:06
# ---------------------------------------------------------------
# please do not use for illegal purposes
# thanks.
# ---------------------------------------------------------------
# idea is based on grabash.py from http://code610.blogspot.com.
# as you can see, opposite to grabash.py,  here we have only a
# 'scan mode', so we will not exploit anything (in default mode).
#
# in OpenVAS you can define credentials as well, so 'post
# exploitation/scanning' should be possible (see man pages).
#
# this code was created only as a proof-of-concept
# ---------------------------------------------------------------
# enjoy ;)
#

# P.S.
# yeah, it's a 'quick&dirty hack' so _a_lot_of_ exception handlers
# is needed, but you can write them as an excercise. ;)
# cheers!
#

import re
import sys
import subprocess

##
# set target host/IP
try:
  target = sys.argv[1]

  ##
  # create target for new scan:
  cmd = "omp -u admin -w letmein --xml='<create_target> <name>"+target+"</name> <hosts>"+target+"</hosts> </create_target>' > tmp.resp"
  runme = subprocess.call([cmd],shell=True)

  readRespForID = open('tmp.resp','r')
  lines = readRespForID.readlines()

  for line in lines:
    # read resp from creating targetID:
    trying = re.compile('create_target_response id="(.*?)"')
    found = re.search(trying, line)

    if found:
      targetID = found.group(1)
      print "[+] Found target ID:" + str(targetID)

  ##
  # prepare scan options (default full scan):
  configID = "daba56c8-73ec-11df-a475-002264764cea" # default mode: full and fast scan ;)
  cmd = "omp -u admin -w letmein --xml='<create_task> <name>Full and fast scan</name> <comment>Full and fast</comment> <config id=\""+ configID +"\"/> <target id=\""+ targetID +"\"/> </create_task>' > tmp.task"

  print '[+] Preparing options for the scan...'
  runme = subprocess.call([cmd],shell=True)

  getTaskID = open('tmp.task','r')
  lines = getTaskID.readlines()

  for line in lines:
    trying = re.compile('create_task_response id="(.*?)"')
    found = re.search(trying, line)

    if found:
      taskID = found.group(1)
      print '[+] Task ID = ', taskID


  ##
  # run prepared taskID for targetID
  print '[+] Running scan for ', target

  # yep, you will be asked for a pass here ;)
  cmd = "omp -u admin --xml='<start_task task_id=\""+ taskID + "\"/>' > tmp.startID"
  runme = subprocess.call([cmd], shell=True)
  print '[+] Scan started... To get current status, type: omp -u admin -G'
  #print '      Have fun ;)\n'

except NameError, e:
  print '[-] TargetID already exists, try different target host/IP'

