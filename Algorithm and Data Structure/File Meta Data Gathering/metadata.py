import csv
import requests
import hashlib
from datetime import date
import os

def loading_file(n):
    # GitHub repository details
    base_url = "https://raw.githubusercontent.com/jimmyislive/sample-files/master/"
    repo_url = os.getenv('GITHUB_REPO_URL', base_url)
    file_name_format = "sample_file_"+str(n)+".txt" 
    # Complete URL for the raw file
    file_url = base_url + file_name_format

    # Send a request to get the content of the file
    response = requests.get(file_url)

    return response, file_name_format

def read_file(response):
        # Check if the request was successful
    if response.status_code == 200:
        body = response.text
    else:
        print(f"Failed to retrieve the file. Status code: {response.status_code}")
    return body

def compute_sha256_hash(response_text):
    data = response_text
    # Encode the data to a bytes object
    encoded_data = data.encode()

    # Create a new SHA256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the bytes from the text
    hash_object.update(encoded_data)

    # Get the hexadecimal digest (the hash value)
    hexdigest = hash_object.hexdigest()
    return hexdigest
    
def save_to_csv():
    data = []
    for items in range(0,20):
        file_loaded = loading_file(items)
        response, file_name = file_loaded[0],file_loaded[1]
        response_text = read_file(response)

        sha256_hexdigest = compute_sha256_hash(response_text)
        file_size = len(response.content)
        word_count = len(response_text.split())
        unique_word_count = len(set(response_text.split()))
        today_date = date.today().strftime("%Y-%m-%d")

        data.append([file_name, sha256_hexdigest, file_size, word_count, unique_word_count, today_date])
        
    header = ["File Name", "SHA256 Hexdigest", "File Size", "Word Count", "Unique Word Count", "Today's Date"]
    
    with open ('interview.csv', 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
        
if __name__ == "__main__":
    save_to_csv()