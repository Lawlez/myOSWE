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
