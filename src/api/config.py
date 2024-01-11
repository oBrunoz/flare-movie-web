from os import environ
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import requests

load_dotenv(find_dotenv(filename='.env'))
api_key = environ.get('API_KEY')
languages = {
    'portuguese': 'pt-BR',
    'english': 'en-US',
}

def getTrending(time_window='week', language='pt-BR', media_type='movie'):
    headers = {
        'Accept': 'application/json',
        'Authorization': api_key,
    }

    URLS = {
        'info': '/{media_type}/{time_window}?{language}&api_key='
    }

    url_trending = f'{environ.get("GET_TRENDING")}{api_key}'
    response = requests.get(url=url_trending, headers=headers)
    json_response = response.json()

    if 'results' in json_response:
        results = json_response['results']

        all_results = []

        for result in results:
            release_date = result.get('release_date')
            date_format = format_release_date(release_date)

            dict_response = {
                'adult': result.get('adult'),
                'backdrop_path': result.get('backdrop_path'),
                'id': result.get('id'),
                'title': result.get('title'),
                'original_language': result.get('original_language'),
                'original_title': result.get('original_title'),
                'overview': result.get('overview'),
                'poster_path': result.get('poster_path'),
                'media_type': result.get('media_type'),
                'genre_ids': result.get('genre_ids'),
                'popularity': result.get('popularity'),
                'release_date': date_format,
                'video': result.get('video'),
                'vote_average': result.get('vote_average'),
                'vote_count': result.get('vote_count'),
            }

            all_results.append(dict_response)

        return all_results

    return None

def format_release_date(release_date):
    if release_date:
        try:
            date_format = datetime.strptime(str(release_date), '%Y-%m-%d').strftime('%d/%m/%Y')
            return date_format
        except ValueError:
            return release_date

    return None
