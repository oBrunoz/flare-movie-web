from os import environ
from src.api.config import api_key, headers

import requests

def getGenreID(genre_id:list, media_type:str, language:str='pt') -> list:
    """
    Retorna os nomes do generos baseado em seus IDS.

    Parameters:
    - genre_id (list): List of genre IDS
    - media_type (str): Type of media ('movie', 'tv')
    - language (str): Language for the genre info (default as Portuguese)

    Returns:
    - list: It returns a list of genre names corresponding to the provided IDs
    """

    id_list = []
    URLS = {
        'genre_url': f'/{media_type}/list?language={language}&api_key='
    }

    url_genre = f'{environ.get("GET_GENRE_MOVIE_LIST")}{URLS["genre_url"]}{api_key}'
    response = requests.get(url=url_genre, headers=headers).json()['genres']

    for genre_data in response:
        if genre_data['id'] in genre_id:
            id_list.append(genre_data['name'])
        else:
            pass

    return id_list