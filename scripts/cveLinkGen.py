import re

# paste any text containing CVE's and i will give you the link for it.
text = """
HTTP Server: source code disclosure with handlers configured via AddType (CVE-2024-40725)
A partial fix for CVE-2024-39884 in the core of Apache HTTP Server 2.4.61 ignores some use of the legacy content-type based configuration of handlers. "AddType" and similar configuration, under some circumstances where files are requested indirectly, result in source code disclosure of local content. For example, PHP scripts may be served instead of interpreted.

Users are recommended to upgrade to version 2.4.62, which fixes this issue.

Reported to security team	2024-07-09
fixed by r1919249 in 2.4.x	2024-07-15
Update 2.4.62 released	2024-07-17
Affects	2.4.60 through 2.4.61
important: Apache HTTP Server: SSRF with mod_rewrite in server/vhost context on Windows (CVE-2024-40898)
SSRF in Apache HTTP Server on Windows with mod_rewrite in server/vhost context, allows to potentially leak NTLM hashes to a malicious server via SSRF and malicious requests.

Users are recommended to upgrade to version 2.4.62 which fixes this issue.

Acknowledgements:

finder: Smi1e (DBAPPSecurity Ltd.)
finder: xiaojunjie (DBAPPSecurity Ltd.)
Reported to security team	2024-07-12
fixed by r1919248 in 2.4.x	2024-07-15
Update 2.4.62 released	2024-07-17
Affects	2.4.0 through 2.4.61
Fixed in Apache HTTP Server 2.4.61
important: Apache HTTP Server: source code disclosure with handlers configured via AddType (CVE-2024-39884)
A regression in the core of Apache HTTP Server 2.4.60 ignores some use of the legacy content-type based configuration of handlers. "AddType" and similar configuration, under some circumstances where files are requested indirectly, result in source code disclosure of local content. For example, PHP scripts may be served instead of interpreted.

Users are recommended to upgrade to version 2.4.61, which fixes this issue.

Reported to security team	2024-07-01
fixed by r1918839 in 2.4.x	2024-07-03
Update 2.4.61 released	2024-07-03
Affects	2.4.60
Fixed in Apache HTTP Server 2.4.60
low: Apache HTTP Server: DoS by Null pointer in websocket over HTTP/2 (CVE-2024-36387)
Serving WebSocket protocol upgrades over a HTTP/2 connection could result in a Null Pointer dereference, leading to a crash of the server process, degrading performance.
"""

cve_pattern = r"(CVE-\d{4}-\d{4,5})"
cves = list(set(re.findall(cve_pattern, text)))

nist_links = {cve: f"https://nvd.nist.gov/vuln/detail/{cve}" for cve in cves}
for cve, link in nist_links.items():
    print(f"{cve}: {link}")
