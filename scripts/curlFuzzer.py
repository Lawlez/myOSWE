import asyncio
import threading
import random  # Using built-in random module
from pwn import log
import aiohttp
import shlex
from urllib.parse import quote

# Define the character sets to use for fuzzing
charsets = {
    'alpha': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'numeric': '0123456789',
    'alphanumeric': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    'special': '!@#$%^&*()-_=+[]{}|;:,.<>?/`~'
}

# Define the range of lengths to use for fuzzing
min_length = 1
max_length = 20

# Define the number of requests to send per thread
num_requests = 3

# Manual CURL parsing function
def parse_curl_command(curl_command):
    curl_command = curl_command.replace('@@', '{}')  # Placeholder for payload injection
    parts = shlex.split(curl_command)
    headers = {}
    data = None
    method = 'GET'
    url = None

    for i in range(len(parts)):
        if parts[i] == 'curl':
            continue
        elif parts[i] == '-X':
            method = parts[i + 1].upper()
        elif parts[i] == '-H':
            header = parts[i + 1].split(':', 1)
            headers[header[0].strip()] = header[1].strip()
        elif parts[i] in ['--data', '--data-raw', '--data-binary']:
            data = parts[i + 1]
            method = 'POST'  # Typically, data in CURL implies a POST request
        elif not parts[i].startswith('-'):
            url = parts[i]

    return url, method, headers, data

# Define the filter function to use
def filter_response(response):
    return response.status != 404  # Example filter logic

# Define the coroutine to make requests
async def make_request(session, url, method, headers, data, payload):
    # URL encode the payload to ensure that special characters are handled correctly
    encoded_payload = quote(payload)
    target_url = url.replace('@@', encoded_payload)  # Direct replacement of the payload

    async with session.request(method, target_url, headers=headers, data=data) as response:
        if filter_response(response):
            log.info(f"URL: {target_url} | Status: {response.status}")
            with open('filtered_responses.txt', 'a') as f:
                f.write(f'{target_url}\n{await response.text()}\n\n')

# Generate and make requests with fuzzing payloads
async def generate_and_make_requests(session, url, method, headers, data):
    for _ in range(num_requests):
        # Generate a random payload using built-in random module
        charset = random.choice(list(charsets.keys()))
        payload = ''.join(random.choice(charsets[charset]) for _ in range(random.randint(min_length, max_length)))
        log.info(f"Generated payload: {payload}")
        await make_request(session, url, method, headers, data, payload)

# Wrapper to handle asyncio event loop for each thread
def thread_worker(curl_command):
    url, method, headers, data = parse_curl_command(curl_command)
    async def run():
        async with aiohttp.ClientSession() as session:
            await generate_and_make_requests(session, url, method, headers, data)
    asyncio.run(run())

# Function to start the fuzzing with multiple threads
def start_fuzzer(curl_command, num_threads=10):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=thread_worker, args=(curl_command,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# Example CURL command with @@ as a placeholder
curl_command = "curl --path-as-is -i -s -k -X $'POST' \
    -H $'Host: thing.com' -H $'Content-Length: 0' -H $'Referer: @@' -H $'Content-Type: application/json' -H $'Accept: */*' -H $'Sec-Fetch-Site: same-origin' -H $'Sec-Fetch-Mode: cors' -H $'Sec-Fetch-Dest: empty' -H $'Accept-Encoding: gzip, deflate, br' -H $'Accept-Language: en-US,en;q=0.9' -H $'Connection: close' \
    $'https://thang.com/api/device/initAuthentication'"

# Start the fuzzer
start_fuzzer(curl_command, num_threads=10)
