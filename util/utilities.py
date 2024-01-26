
import requests

def download(url, destination):
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"Download successful. File saved to: {destination}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
