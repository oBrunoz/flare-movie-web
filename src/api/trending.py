from os import environ
from src.api.config import api_key, headers, format_release_date, truncate_text
from src.api.genre import getGenreID

import requests

def getTrending(time_window:str='week', language:str='pt-BR', media_type:str='movie', max_text_length:int=120):
    URLS = {
        'trending_media': f'/trending/{media_type}/{time_window}?language={language}&api_key='
    }

    url_trending = f'{environ.get("GET_BASE_URL")}{URLS["trending_media"]}{api_key}'
    response = requests.get(url=url_trending, headers=headers).json()

    if 'results' in response:
        results = response['results']

        all_results = []

        for result in results:
            response_media_type = result.get('media_type')
            release_date = result.get('release_date') if result.get('release_date') is not None else result.get('first_air_date')
            date_format = format_release_date(release_date)
        
            response_ids = result.get('genre_ids')
            genre_names = getGenreID(genre_ids=response_ids, media_type=response_media_type)

            dict_response = {
                'adult': result.get('adult'),
                'backdrop_path': result.get('backdrop_path'),
                'id': result.get('id'),
                'title': result.get('title') if result.get('title') is not None else result.get('name'),
                'original_language': result.get('original_language'),
                'original_title': result.get('original_title'),
                'overview': truncate_text(result.get('overview'), max_text_length),
                'poster_path': result.get('poster_path'),
                'media_type': result.get('media_type'),
                'genre_ids': genre_names,
                'popularity': result.get('popularity'),
                'release_date': date_format[0],
                'release_year': date_format[1],
                'video': result.get('video'),
                'vote_average': round(result.get('vote_average'), 1),
                'vote_count': result.get('vote_count'),
            }

            all_results.append(dict_response)

        return all_results