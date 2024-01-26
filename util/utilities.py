
import requests

def download(url, destination):
    """
    Downloads a file from the given URL and saves it to the specified destination.

    Args:
        url (str): The URL of the file to download.
        destination (str): The path where the file will be saved.

    Returns:
        None
    """
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"Download successful. File saved to: {destination}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

