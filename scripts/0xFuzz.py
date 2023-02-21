import requests
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
num_requests = 400

# Define the filter function to use
def filter_response(response):
    # Here you can define any logic to filter the response.
    # This example simply filters out responses with a 404 status code.
    return response.status_code != 200

# Define the worker function to send requests and filter responses
def worker():
    while True:
        # Generate a random payload
        length = random.randint(min_length, max_length)
        charset = random.choice(list(charsets.keys()))
        payload = ''.join(random.choice(charsets[charset]) for _ in range(length))
        print(payload)
        # Send the request
        full_url = url + payload
        response = requests.get(full_url)

        # Filter the response
        if filter_response(response):
            # Save the filtered response to a file
            with open('filtered_responses.txt', 'a') as f:
                f.write(f'{full_url}\n{response.headers}\n{response.content}\n')

        # Check if we've sent enough requests
        with lock:
            global requests_sent
            requests_sent += 1
            if requests_sent >= num_requests:
                break

# Create the threads and start them
num_threads = 200
requests_sent = 0
lock = threading.Lock()
threads = []
for i in range(num_threads):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()
