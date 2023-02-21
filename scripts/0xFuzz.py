import requests
import random
import string

#Define the URL to fuzz
url = 'http://example.com/page?param='

#Define the character sets to use for fuzzing
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
num_requests = 100

# Define the filter function to use
def filter_response(response):
    # Here you can define any logic to filter the response.
    # This example simply filters out responses with a 404 status code.
    return response.status_code != 404

# Send the requests and filter the responses
for i in range(num_requests):
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
            f.write(f'{full_url}\n{response.text}\n\n')
