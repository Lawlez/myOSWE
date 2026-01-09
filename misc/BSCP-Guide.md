# Exam Introduction & Structure

You will have **four hours** to complete the Burp Suite Certified Practitioner exam. There are **two applications**, and each application contains deliberate vulnerabilities. This means that each application can be **completed in three stages**:

1. **Stage 1**: Access any user account.
2. **Stage 2**: Use your user account to access the admin interface at /admin, perhaps by elevating your privileges or compromising the administrator account.
3. **Stage 3**: Use the admin interface to read the contents of /home/carlos/secret from the server's filesystem, and submit it using "submit solution".

The three stages are to be completed in order. This means that if you are in an application, attempting to break into the admin interface is a waste of time if you haven't yet got access to a user account. Likewise, we do not recommend attempting to read files if you don't have access to an admin account.

We **restrict outbound traffic** from the vulnerable servers to the **internet**. You won't be able to connect back to any internet server, **except** for the public **Burp Collaborator** server and the integrated exploit server. You can use the integrated exploit server to deliver any kind of payload to the vulnerable application or simulated user.

Although some of the **vulnerabilities are tricky** to find, we **do not intentionally hide files or pages** that contain them. You **never need to guess folders, filenames or parameter** names.

> In this exam you need to Identify possible vulnerabilities quickly, and exploit them as much as possioble, usually every stage reveals a new vulnerable function or service.
> 

To achieve this, you have to make smart use of burps scanner in combination with your manual testing.

## How to prepare for the exam

- Do all the academy labs until you are confident at Practitioneer level. (f.e. my lab progress is only at 38%)
- Do at least 10 - 20 unsolved and solved Mistery Labs https://portswigger.net/web-security/mystery-lab-challenge
- Take the Prep Exam 1 & 2 as often as possible until you can easily do them in less than 2h. i probably did them like 5 times each
- Take your own notes, especially for topics you are not too confident.
- Collect base payloads during your learning, as those can be used and modified during the test.
- Learn about Obfuscation: https://portswigger.net/web-security/essential-skills/obfuscating-attacks-using-encodings
- Learn about targeted scanning: https://portswigger.net/web-security/essential-skills/using-burp-scanner-during-manual-testing

## Requirements for your setup before starting the exam

- Burp Suite Pro
- ysoserial setup and running (works best in older java env)
- SQLMap (optional if u like it)

**Burp Plugins:**

- HTTP Request Smuggler
- Java Deserialisation Scanner (optional but easier)
- Auth Analyzer
- Collaborator Everywhere (run once)
- InQL (in case of graphQL)
- ActiveScan++ (optional)
- Server-Side Prototype Pollution Scanner (optional)

Make sure you have the required tools installed and you know how to set them up and work with them, you will not have time to fix it or figure it out during the exam.

**Make use of Burp Pro Tools:**

- CSRF PoC
- Burp Scanner (targeted)
- Scan selected insertion point
- Burp Collaborator

Have the Academy Page open and use the labs solutions when you are stuck at a vulnerability.

## Stages of the exam and its Vulnerabilities

**FOOTHOLD - Stage 1**

- Content Discovery
- DOM-XSS
- XSS Cross Site Scripting
- Web Cache Poison
- Password Reset
- Host Headers
- HTTP Request Smuggling
- Brute force
- Authentication

**PRIVILEGE ESCALATION - Stage 2**

- CSRF - Account Takeover
- Password Reset
- SQLi - SQL Injection
- JWT - JSON Web Tokens
- Prototype pollution
- API Testing
- Access Control
- GraphQL API Endpoints
- CORS - Cross-origin resource sharing

**DATA EXFILTRATION - Stage 3**

- XXE - XML entities & Injections
- SSRF - Server side request forgery
- SSTI - Server side template injection
- SSPP - Server Side Prototype Pollution
- LFI - File path traversal
- File Uploads
- Deserialization
- OS Command Injection

**Possible Vulnerabilities per stage:**

So for example if you find some serialization during phase 1 its like its not used in that phase or maybe not at all, since this type is only used in Stage 3 in the BSCP environment.

## My Exam Labs

### First Try

**App1**:

- Stage1: XSS combined with Request smuggling
- Stage2: HTTP Request smuggling to get cookie
- Stage3: Blind XXE - exfiltrate local files

**App2**:

- Stage1: Bruteforce on Login
- Stage2: Insecure deserialization java
- Stage3: Blind Error based XXE (not solved)

### Second Try

**App1**:

- Stage1: Bruteforce on Login
- Stage2: CORS misconfiguration on API (dont remeber what exactly it was)
- Stage3: Blind XXE - exfiltrate local files (not solved)

**App2**:

- Stage1: Host Header Injection on reset password
- Stage2: Mass Assignment on user object
- Stage3: Exploit known third party vulnerability in wkhtmltopdf to exfiltrate local files

### Third Try

**App1**:

- Stage1: Reflected XSS - Cookie stealer
- Stage2: ?? dunno but must have been easy since i went straight to admin
- Stage3: Exploit known third party vulnerability in imagick to exfiltrate local files

**App2**:

- Stage1: Host Header Injection on reset password
- Stage2: Blind SQLi on search
- Stage3: Blind XXE with external dtd

As you can see very common were: Brute Force, Host header injection, as well as XXE

| **Resource** | **URL** |
| --- | --- |
| BSCP Exam Hints | https://portswigger.net/web-security/certification/exam-hints-and-guidance |
| Learning resource | https://bscp.guide/ |
| Password list for exam | https://portswigger.net/web-security/authentication/auth-lab-passwords |
| User List for exam | https://portswigger.net/web-security/authentication/auth-lab-usernames |