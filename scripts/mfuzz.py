import asyncio
import aiohttp
import random
import string
import threading

# Define the URL to fuzz
url = 'http://example.com/page?param='

# Define the character sets to use for fuzzing
charsets = {
    'alpha': string.ascii_letters,
    'numeric': string.digits,
    'alphanumeric': string.ascii_letters + string.digits,
    'special': string.punctuation
}

# Define the range of lengths to use for fuzzing
min_length = 1
max_length = 20

# Define the number of requests to send
num_requests = 3

# Define the filter function to use
def filter_response(response):
    # Here you can define any logic to filter the response.
    # This example simply filters out responses with a 404 status code.
    return response.status != 404

# Define the coroutine to make requests
async def make_request(payload):
    async with aiohttp.ClientSession() as session:
        full_url = url + payload
        async with session.get(full_url) as response:
            if filter_response(response):
                # Save the filtered response to a file
                with open('filtered_responses.txt', 'a') as f:
                    f.write(f'{full_url}\n{await response.text()}\n\n')

# Define the function to generate payloads and make requests
def generate_and_make_requests():
    for i in range(num_requests):
        # Generate a random payload
        length = random.randint(min_length, max_length)
        charset = random.choice(list(charsets.keys()))
        payload = ''.join(random.choice(charsets[charset]) for _ in range(length))
        print(payload)
        # Make the request
        asyncio.run(make_request(payload))

# Create and start the threads
threads = []
num_threads = 300
for i in range(num_threads):
    thread = threading.Thread(target=generate_and_make_requests)
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()
