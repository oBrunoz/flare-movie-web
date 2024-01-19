from os import environ
from src.api.config import api_key, headers, format_release_date, convert_minutes_to_hours
from random import randrange
import requests


def getMediaImages(media_id:int, media_type:str, language:str='en', get_random_backdrop:bool=False) -> list:
    URLS = {
        'image_details': f'/{media_type}/{media_id}/images?language={language}&api_key='
    }

    url_media_detail = f'{environ.get("GET_MEDIA_IMAGES")}{URLS["image_details"]}{api_key}'

    try:
        response = requests.get(url=url_media_detail, headers=headers)
        response.raise_for_status()
        data = response.json()

        backdrop_file_paths = [item['file_path'] for item in data['backdrops']]
        logo_file_paths = [item['file_path'] for item in data['logos']]

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


def getMediaDetails(media_id: int, media_type: str, language: str = 'pt-BR') -> dict:
    URLS = {
        'media_details': f'/{media_type}/{media_id}?language={language}&api_key='
    }

    url_media_detail = f'{environ.get("GET_MEDIA_DETAILS")}{URLS["media_details"]}{api_key}'
    response = requests.get(url=url_media_detail, headers=headers).json()

    random_image_path, logo_image_path = getMediaImages(media_id, media_type, get_random_backdrop=True)

    media_details = {
        'adult': response.get('adult', False),
        'backdrop_path': response.get('backdrop_path', None),
        'logo_path': logo_image_path[0] if logo_image_path and len(logo_image_path) > 0 else None,
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
        'runtime_hour': convert_minutes_to_hours(response.get('runtime')),
        'spoken_languages': [{'english_name': lang['english_name'], 'iso_639_1': lang['iso_639_1'], 'name': lang['name']} for lang in response.get('spoken_languages', [])],
        'status': response.get('status', ''),
        'tagline': response.get('tagline', ''),
        'title': response.get('title') if response.get('title') is not None else response.get('name'),
        'video': response.get('video', False),
        'vote_average': round(response.get('vote_average'), 1) if response.get('vote_average') else None,
        'vote_count': response.get('vote_count', 0),
    }

    return media_details
