import asyncio
import aiohttp
import random
import string
import threading
import re

# Your curl command with payload placeholder (marked with @@ for fuzzing)
curl_command = "curl --path-as-is -i -s -k -X $'POST' \
    -H $'Host: mobileappdashboard-uat.juliusbaer.com' -H $'Content-Length: 0' -H $'Referer: @@' -H $'Content-Type: application/json' -H $'Accept: */*' -H $'Sec-Fetch-Site: same-origin' -H $'Sec-Fetch-Mode: cors' -H $'Sec-Fetch-Dest: empty' -H $'Accept-Encoding: gzip, deflate, br' -H $'Accept-Language: en-US,en;q=0.9' -H $'Connection: close' \
    $'https://mobileappdashboard-uat.juliusbaer.com/api/device/initAuthentication'"

proxy_url = "http://127.0.0.1:8080"
custom_ssl_cert_path = None  # Set to your custom SSL certificate path if needed

# Parse the cURL command to extract method, headers, and URL
def parse_curl_command(command):
    method = re.search(r"-X \$'(\w+)'", command).group(1)
    url = re.search(r"\$'(https?://[^\s]+)'", command).group(1)
    headers = dict(re.findall(r"-H \$'([^:]+):\s?([^']+)'", command))
    return method, url, headers

method, url, headers = parse_curl_command(curl_command)

# Define the character sets to use for fuzzing
charsets = {
    'alpha': string.ascii_letters,
    'numeric': string.digits,
    'alphanumeric': string.ascii_letters + string.digits,
    'special': string.punctuation
}

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
async def generate_and_make_requests(session, url, method, headers, data, proxy_url):
    while True:
        length = random.randint(min_length, max_length)
        charset = random.choice(list(charsets.keys()))
        payload = ''.join(random.choice(charsets[charset]) for _ in range(length))

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
            task = generate_and_make_requests(session, url, method, headers, None, proxy_url)
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
