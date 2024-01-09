from os import environ
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import requests
import json

load_dotenv(find_dotenv(filename='.env'))
api_key = environ.get('API_KEY')
languages = {
    'portuguese': 'pt-BR',
    'english': 'en-US',
}

def dateFormat(date, language='pt-BR'):
    if language == languages['portuguese']:
        release_date_datetime = datetime.strptime(date, '%Y-%m-%d')
        formated_release_date = release_date_datetime.strftime('%d/%m/%Y')
    elif language == languages['english']:
        formated_release_date = datetime.strptime(date, '%Y-%m-%d')
    else:
        return json({'error': 'Language not found.'})

    return formated_release_date

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

        if results:
            # Itera sobre cada item em 'results'
            for result in results:
                # Extrai informações desejadas para o dicionário
                release_movie_date = result.get('release_date', None)

                if release_movie_date is not None:
                    date_format = dateFormat(str(release_movie_date))

                dict_response = {
                    'adult': result.get('adult', None),
                    'backdrop_path': result.get('backdrop_path', None),
                    'id': result.get('id', None),
                    'title': result.get('title', None),
                    'original_language': result.get('original_language', None),
                    'original_title': result.get('original_title', None),
                    'overview': result.get('overview', None),
                    'poster_path': result.get('poster_path', None),
                    'media_type': result.get('media_type', None),
                    'genre_ids': result.get('genre_ids', None),
                    'popularity': result.get('popularity', None),
                    'release_date': date_format,
                    'video': result.get('video', None),
                    'vote_average': result.get('vote_average', None),
                    'vote_count': result.get('vote_count', None),
                }

                # Adiciona o dicionário à lista
                all_results.append(dict_response)
        else:
            all_results.append({'error': 'error'})
        
        return all_results

    return None
