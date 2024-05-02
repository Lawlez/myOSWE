import requests

# Set the target URL
url = "http://68.219.58.184/"

# Define headers and data to send
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://68.219.58.184",
    "Referer": "http://68.219.58.184/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
data = {
    "vote": "Dogs"
}

# Send the request 3000 times
for _ in range(3000):
    response = requests.post(url, headers=headers, data=data)
    # Print response status code to monitor progress/errors
    print(response.status_code)

