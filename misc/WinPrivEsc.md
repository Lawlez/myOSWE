# Windows Privilege escalation help guide

## collect sysinfo:
`systeminfo > systeminfo.txt`

## Run wes:

```
  wes.py systeminfo.txt
  
  # Only show vulnerabilities of a certain impact
  
  wes.py systeminfo.txt -i "Remote Code Execution"

  # Only show vulnerabilities of a certain severity
  wes.py systeminfo.txt -s critical
```

## Look for free credentials using LaZagne:

https://github.com/AlessandroZ/LaZagne

Run:
`laZagne.exe all`