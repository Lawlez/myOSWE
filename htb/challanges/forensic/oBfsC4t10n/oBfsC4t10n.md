---
title: oBfsC4t10n
description: A write up for the oBfsC4t10n challenge
published: false
datePublished: 1610805690979
author: lwlx
authorTwitter: "0x0000005"
authorPhoto: /profile.jpg
tags:
  - ctf
  - writeup
  - hackthebox
  - oBfsC4t10n
  - htb
  - security
thumbnailPhoto: /hackerone/hackerone.png
bannerPhoto: /hackerone/hackerone.png
canonicalUrl:
---

# oBfsC4t10n _[HARD]_

This is my Write Up for the "oBfsC4t10n" challenge from Hack The Box.

we get a zip file. after extraction we are presented with an html file telling us to download an excel file.
The excel file has been included in the html as a base64 encoded string, lets just save that info for later base64.txt.

so after we checked the html and demed the download save lets fetch the excel file.

## Enumeration

Instead ofn trying to open or analyze the file on my machine, lets go ahead and upload it to ANY.RUN.

> ANY.RUN is a online Sandbox service that allows you to open various suspicious files or programms to fully analyze what would happen.

After Testing the file with AN.RUN we were able to see how the exploit would work and what would be done.

We tested on a Windows 7 Machine, after opening the file, the exploit imediately startet to run:

At first a temp file was created under `C:\Users\admin\AppData\Local\Temp\CVR40EB.tmp.cvr`
Then a what seems to be `visual basic script` executer was added here: `C:\Users\admin\AppData\Local\Temp\VBE\MSForms.exd`
followed by a `.hta` file with a funny name..: `C:\Users\admin\AppData\Local\Temp\LwTHLrGh.hta` <-- lemme guess thats the one.
it then makes use of `mshta.exe` to try and execute the `LwTHLrGh.hta` file.

here ANY.RUN stops executing the file.

I went ahead and downloaded the `MSForms.exd` as well as the `LwTHLrGh.hta` file so we can analyze them further.

## Analyzing `LwTHLrGh.hta`

```

```
