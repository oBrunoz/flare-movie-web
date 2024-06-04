from os import environ
from src.api.Config import api_key, headers, format_release_date, convert_minutes_to_hours
from random import randrange
import requests

def getMediaImages(media_id:int, media_type:str, language:str='en', get_random_backdrop:bool=False) -> list:
    URLS = {
        'image_details': f'/{media_type}/{media_id}/images?language={language}&api_key='
    }

    url_media_detail = f'{environ.get("GET_BASE_URL")}{URLS["image_details"]}{api_key}'

    try:
        response = requests.get(url=url_media_detail, headers=headers)
        response.raise_for_status()
        data = response.json()

        
        backdrop_file_paths = [item['file_path'] for item in data.get('backdrops')]
        logo_file_paths = [item['file_path'] for item in data.get('logos')]

        if get_random_backdrop and backdrop_file_paths:
            random_index = randrange(len(backdrop_file_paths))
            random_backdrop_path = backdrop_file_paths[random_index]

            return random_backdrop_path, logo_file_paths

        return backdrop_file_paths, logo_file_paths

    except requests.exceptions.RequestException as e:
        print(f'Error fetching media images: {e}')
        return None, None
    except Exception as e:
        print(f'An expected error has ocurred. Error detail: {e}')