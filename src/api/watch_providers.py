from os import environ
from src.api.config import api_key, headers
import requests

def getWatchProviders(media_id:int, media_type:str, country:str='BR'):
    URLS = {
        'watch_providers': f'/{media_type}/{media_id}/watch/providers?api_key='
    }

    url_media_provider = f'{environ.get("GET_BASE_URL")}{URLS["watch_providers"]}{api_key}'

    try:
        response = requests.get(url=url_media_provider, headers=headers)
        response.raise_for_status()
        data = response.json()

        if 'results' in data:
            data_map = data['results'][country]

            

            return data['results'][country]

    except Exception as e:
        print(e)