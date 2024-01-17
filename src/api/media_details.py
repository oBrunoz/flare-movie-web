from os import environ
from src.api.config import api_key, headers, format_release_date, truncate_text
import requests

def getMediaDetails(media_id:int, media_type:str, language:str='pt-BR') -> dict:
    URLS = {
        'media_details': f'/{media_type}/{media_id}?language={language}&api_key='
    }

    url_media_detail = f'{environ.get("GET_MEDIA_DETAILS")}{URLS["media_details"]}{api_key}'
    response = requests.get(url=url_media_detail, headers=headers).json()

    media_details = {
        'adult': response.get('adult', False),
        'backdrop_path': response.get('backdrop_path', ''),
        'belongs_to_collection': response.get('belongs_to_collection', None),
        'budget': response.get('budget', 0),
        'genres': [{'id': genre['id'], 'name': genre['name']} for genre in response.get('genres', [])],
        'homepage': response.get('homepage', ''),
        'id': response.get('id', 0),
        'imdb_id': response.get('imdb_id', ''),
        'original_language': response.get('original_language', ''),
        'original_title': response.get('original_title', ''),
        'overview': response.get('overview', ''),
        'popularity': response.get('popularity', 0.0),
        'poster_path': response.get('poster_path', ''),
        'production_companies': [{'id': company['id'], 'logo_path': company['logo_path'], 'name': company['name'], 'origin_country': company['origin_country']} for company in response.get('production_companies', [])],
        'production_countries': [{'iso_3166_1': country['iso_3166_1'], 'name': country['name']} for country in response.get('production_countries', [])],
        'release_date': format_release_date(response.get('release_date', '')),
        'revenue': response.get('revenue', 0),
        'runtime': response.get('runtime', 0),
        'spoken_languages': [{'english_name': lang['english_name'], 'iso_639_1': lang['iso_639_1'], 'name': lang['name']} for lang in response.get('spoken_languages', [])],
        'status': response.get('status', ''),
        'tagline': response.get('tagline', ''),
        'title': response.get('title', ''),
        'video': response.get('video', False),
        'vote_average': response.get('vote_average', 0.0),
        'vote_count': response.get('vote_count', 0),
    }

    return media_details
