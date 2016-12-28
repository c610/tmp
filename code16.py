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

# changelog:
#   28.12.16 - added: reports to pdf ;P

import re
import sys
import subprocess
import time
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
  print '[+] Scan started... To get current status, see below:'# or type: omp -u admin -G'

  # sleep few secs to get -G with our target:
  time.sleep(3)

  cmd2 = "omp -u admin -w letmein -G | grep %s > tmp.stat" % ( taskID)
  # print cmd2
  runme = subprocess.call([cmd2],shell=True)


  while 'Done' not in open('tmp.stat','r').read():
    print '[?]   ...zZzZZzZz...'
    time.sleep(1)
    runme = subprocess.call([cmd2],shell=True)


  print '[+] Scan looks to be done. Good.'

  # target/taskID is scanned. rewriting results to report:
  print '[+] Target scanned. Finished taskID : ' + str(taskID)

  # reports
  print '[+] Cool! We can generate some reports now ... :)'

  getXml = "omp -u admin -w letmein -X '<get_reports/> <report id><task id=\""+ str(taskID)  +"\"/>' > get.xml"
  #print getXml

  rungetXml = subprocess.call([getXml],shell=True)
  print '[+] Looking for report ID...'

  lookingFor = '<report id="(.*?)" format_id="(.*?)<task id="' + str(taskID) + '"'
#  print lookingFor

  xml = open('get.xml','r')
  xlines = xml.readlines()

  for xline in xlines:
    match = re.compile(lookingFor)
    found = re.search(match, xline)

    if found:
      repID = found.group(1)
      print '  [+] Found report ID : ' + repID
      print '  [+] For taskID      : ' + taskID

      print ''
      print '[+] Preparing report in PDF for %s ' % target
      repName = 'Report_for_'+str(target)+'.pdf'

      getRep = ("omp -u admin -w letmein --get-report %s --format c402cc3e-b531-11e1-9163-406186ea4fc5 > %s") % (repID, repName)

      runme = subprocess.call([getRep],shell=True)

      print '[+] Report should be done in : ', repName
      # todo: check via sth like ls-la if rep.pdf is there

  print '[+] Thanks. Cheers!\n'
  #print '      Have fun ;)\n'

except NameError, e:
  print '[-] TargetID already exists, try different target host/IP'
  pass
