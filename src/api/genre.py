from os import environ
from src.api.config import api_key, headers

import requests

def getGenreID(genre_ids:list, media_type:str, language:str='pt') -> list:
    """
    Retorna os nomes do generos baseado em seus IDS.

    Parameters:
    - genre_id (list): List of genre IDS
    - media_type (str): Type of media ('movie', 'tv')
    - language (str): Language for the genre info (default as Portuguese)

    Returns:
    - list: It returns a list of genre names corresponding to the provided IDs
    """

    URLS = {
        'genre_url': f'/genre/{media_type}/list?language={language}&api_key='
    }

    url_genre = f'{environ.get("GET_BASE_URL")}{URLS["genre_url"]}{api_key}'
    response = requests.get(url=url_genre, headers=headers)
    
    response.raise_for_status()
    data = response.json()

    genre_dict = {genre_data['id']: genre_data['name'] for genre_data in data['genres']}
    genre_names = [genre_dict.get(genre_id) for genre_id in genre_ids]
    genre_names = [name for name in genre_names if name is not None]

    return genre_names