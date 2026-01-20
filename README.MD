<h1 style="margin:20%">Offensive Security</h1>

---

## About

My collection of useful resources, tools and solutions used for Pentesting or security assessments. 

- [x] **htb**: contains files and writeups for various hackthebox challenges and machines. Usually the solution is not included ;)
- [x] **lists**: contains various Fuzzing and payload lists used for pentesting
- [x] **misc**: miscallenous files that dont fit anywhere else, f.e. Report template
- [x] **pdf**: Various PDF files, Cheatsheets, writeups and other pdfs worht to look at
- [x] **scripts**: contains helpful scripts mostly used for pentesting but also some other stuff, also contains CVE PoC's and duckyscripts
- [x] **pentestfiles**: contains ready to use files to use as payloads, especially for file upload attacks. Contains shells, EICAR files, and various other special files.


Originally in this repository I documented my jorney to becoming an Offensive Security Web Expert (OSWE). Currently im using this repository as a one stop shop for all my IT & Security needs.

------------------------------------------------------------------------------------------
<br/>


## Tools

- [x] ([CyberChef](https://cyberchef.cybertap.ch)) a web app for encryption, encoding, compression and data analysis
- [x] ([JSNICE](http://jsnice.org/)) a JavaScript Deobfuscation tool
- [x] ([boxentriq/code-breaking](https://www.boxentriq.com/code-breaking)) various codebreaking and cipher tools
- [x] ([SSLLabs](https://www.ssllabs.com/ssltest/analyze.html)) Test SSL of any webserver
- [x] ([deps.dev](https://deps.dev/)) Understand your dependencies
- [x] ([dehashed.com](https://dehashed.com/)) Leaked Passwords in plaintext
- [x] ([Regex101](https://regex101.com/)) a Regex Helper Tool
- [x] ([Hackthebox Academy](https://academy.hackthebox.com/)) Best place to learn new CyberSec skills.
- [x] ([Web Proxy](https://removepaywalls.com/2/https://hackthebox.com)) Cant access websites, try this.
- [x] ([Hudson Rock](https://www.hudsonrock.com/threat-intelligence-cybercrime-tools)) Free Infostealer intelligence toolset


<br/>

## Cheatsheets and misc

### cURL cheatsheet

<table style="font-size: 11px">
<thead>
<tr>
<th><strong>Command</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>curl http://lwlx.xyz</code></td>
<td>GET request with <code>cURL</code></td>
</tr>
<tr>
<td><code>curl http://lwlx.xyz -v</code></td>
<td>Verbose GET request with <code>cURL</code></td>
</tr>
<tr>
<td><code>curl http://admin:password@lwlx.xyz/ -vvv</code></td>
<td><code>cURL</code> Basic Auth login</td>
</tr>
<tr>
<td><code>curl -u admin:password http://lwlx.xyz/ -vvv</code></td>
<td>Alternate <code>cURL</code> Basic Auth login</td>
</tr>
<tr>
<td><code>curl -u admin:password -L http://lwlx.xyz/</code></td>
<td><code>cURL</code> Basic Auth login, follow redirection</td>
</tr>
<tr>
<td><code>curl -u admin:password 'http://lwlx.xyz/search.php?port_code=us'</code></td>
<td><code>cURL</code> GET request with parameter</td>
</tr>
<tr>
<td><code>curl -d 'username=user&amp;password=pass' -L http://lwlx.xyz/login.php</code></td>
<td>POST request with <code>cURL</code></td>
</tr>
<tr>
<td><code>curl -d 'username=user&amp;password=pass' -L http://lwlx.xyz/login.php -v</code></td>
<td>Debugging with <code>cURL</code></td>
</tr>
<tr>
<td><code>curl -d 'username=user&amp;password=pass' -L --cookie-jar /dev/null http://lwlx.xyz/login.php -v</code></td>
<td>Cookie usage with <code>cURL</code></td>
</tr>
<tr>
<td><code>curl -d 'username=user&amp;password=pass' -L --cookie-jar cookies.txt http://lwlx.xyz/login.php</code></td>
<td><code>cURL</code> with cookie file</td>
</tr>
<tr>
<td><code>curl -H 'Content-Type: application/json' -d '{ "username" : "user", "password" : "pass" }'</code></td>
<td><code>cURL</code> specify content type</td>
</tr>
<tr>
<td><code>curl -X OPTIONS http://lwlx.xyz/ -vv</code></td>
<td><code>cURL</code> OPTIONS request</td>
</tr>
<tr>
<td><code>curl -X PUT -d @test.txt http://lwlx.xyz/test.txt -vv</code></td>
<td>File upload with <code>cURL</code></td>
</tr>
<tr>
<td><code>curl -X DELETE http://lwlx.xyz/test.txt -vv</code></td>
<td>DELETE method with <code>cURL</code></td>
</tr>
</tbody>
</table>
<br/>

### shell script brackets cheatsheet

![shell script brackets](./shell-script-brackets.jpeg)
