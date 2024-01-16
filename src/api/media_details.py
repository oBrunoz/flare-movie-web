from os import environ
from src.api.config import api_key, headers, format_release_date, truncate_text


def getMediaDetails(movie_id:int, media_type:str, language:str='pt-BR'):
    URLS = {
        'info': f'/{media_type}/{movie_id}?language={language}&api_key='
    }
    

    return 'a'