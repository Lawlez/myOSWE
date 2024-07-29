import requests

def fetch_license_urls(file_path, output_file):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    
    with open(output_file, 'w') as output:
        for url in urls:
            url = url.strip()
            license_url = url + '.LICENSE.txt'
            try:
                response = requests.get(license_url)
                if response.status_code == 200:
                    output.write(f"License for {url}:\n")
                    output.write(response.text[:200])
                    output.write("\n++++++++++++++++++++++++\n")
                else:
                    output.write(f"Failed to fetch license for {url}\n++++++++++++++++++++++++\n")
            except requests.exceptions.RequestException as e:
                output.write(f"Error fetching license for {url}: {e}\n++++++++++++++++++++++++\n")

fetch_license_urls('urls.txt', 'licenses.txt')
