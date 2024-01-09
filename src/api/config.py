from os import environ
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = environ.get('API_KEY')

def apiGetTrending():
    headers = {
        'Accept': 'application/json',
        'Authorization': api_key,
    }

    url_trending = f'{environ.get("GET_TRENDING")}{api_key}'
    response = requests.get(url=url_trending, headers=headers)

    json_response = response.json()

    if 'results' in json_response:
        results = json_response['results']

        all_results = []

        # Itera sobre cada item em 'results'
        for result in results:
            # Extrai informações desejadas para o dicionário
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
                'release_date': result.get('release_date', None),
                'video': result.get('video', None),
                'vote_average': result.get('vote_average', None),
                'vote_count': result.get('vote_count', None),
            }

            # Adiciona o dicionário à lista
            all_results.append(dict_response)

        return all_results

    return None
