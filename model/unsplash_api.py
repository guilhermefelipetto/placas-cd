"""unsplash api para download das imagens negativas"""

import requests
import time
from random import choice


def search_images(query, access_key, max_requests, per_page=25):
    url = 'https://api.unsplash.com/search/photos'
    headers = {
        'Authorization': f'Client-ID {access_key}'
    }
    total_images_downloaded = 0
    for page in range(1, (max_requests // per_page) + 1):
        params = {
            'query': query,
            'page': page,
            'per_page': per_page
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            images = response.json()['results']
            download_images(images)
            total_images_downloaded += len(images)
            if total_images_downloaded >= max_requests:
                break
        
        else:
            print(f'erro {response.status_code}')
            break


def download_images(images):
    i = 0
    for image in images:
        image_url = image['urls']['regular']
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            filename = image['id'] + f'_{i}' + f'{choice(range(10000, 99999))}' + '.jpg'
            with open(f'negatives\\{filename}', 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
                    i += 12
                print(f'downloaded: {filename}')
                time.sleep(0.1)

max_requests = 50000
access_key = '[key]'
search_images('urban shopping', access_key, max_requests)
