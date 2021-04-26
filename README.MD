<h1 style="margin:20%">Offensive Security</h1>

---

## About

In this repository I document my jorney to becoming an Offensive Security Web Expert (OSWE). Furthermore I will publish an helpful tools or media I found as well as code I wrote during this time in this repository.

---
<br/>

## Tools

- [x] ([CyberChef](https://gchq.github.io/CyberChef/)) a web app for encryption, encoding, compression and data analysis
- [x] ([JSNICE](http://jsnice.org/)) a JavaScript Deobfuscation tool
- [x] ([boxentriq/code-breaking](https://www.boxentriq.com/code-breaking)) various codebreaking and cipher tools

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
