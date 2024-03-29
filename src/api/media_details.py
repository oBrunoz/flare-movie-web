from os import environ
from src.api.config import api_key, headers, format_release_date, convert_minutes_to_hours
from src.api.watch_providers import getWatchProviders
from random import randrange
import requests

def getMediaVideos(media_id:int, media_type:str, language:str='pt-BR'):
    URLS = {
        'media_videos': f'/{media_type}/{media_id}/videos?language={language}&include_video_language=pt-BR,en&api_key=',
        'youtube': 'https://www.youtube.com/embed/'
    }

    url_media_detail = f'{environ.get("GET_BASE_URL")}{URLS["media_videos"]}{api_key}'

    try:
        response = requests.get(url=url_media_detail, headers=headers)
        response.raise_for_status()
        data = response.json()
        videos_pt = []
        videos_en = []

        if 'results' in data:
            for video in data['results']:
                video_name = video.get('name', 'Trailer')
                video_key = video.get('key')
                video_type = video.get('type')
                video_iso = video.get('iso_639_1')

                if video_iso == 'pt':
                    if video_type.lower() == 'trailer':
                        if video_name.startswith("Trailer Oficial") or video_name.startswith("Oficial"):
                            if video_key:
                                youtube_link = f'{URLS["youtube"]}{video_key}'
                                videos_pt.append({'name': video_name, 'youtube_link': youtube_link})
                        else:
                            if video_key:
                                youtube_link = f'{URLS["youtube"]}{video_key}'
                                videos_pt.append({'name': video_name, 'youtube_link': youtube_link})
                elif video_iso == 'en':
                    if video_type.lower() == 'trailer':
                        if video_key:
                            youtube_link = f'{URLS["youtube"]}{video_key}'
                            videos_en.append({'name': video_name, 'youtube_link': youtube_link})
        print(videos_pt)
        print(videos_en)
        return videos_pt, videos_en
    except Exception as e:
        print(e)

def getMediaCredits(media_id:int, media_type:str):
    URLS = {   
        'media_details': f'/{media_type}/{media_id}/credits?api_key='
    }

    url_media_detail = f'{environ.get("GET_BASE_URL")}{URLS["media_details"]}{api_key}'

    try:
        response = requests.get(url=url_media_detail, headers=headers)
        response.raise_for_status()
        data = response.json()
        data_cast = []
        data_crew = []
        director_crew = []

        if 'cast' in data:
            for data_ in data['cast']:
                cast_id = data_['id']
                cast_name = data_['name']
                cast_department = data_['known_for_department']
                profile_path = data_['profile_path']
                cast_character = data_['character']

                data_cast.append({'id': cast_id, 'name': cast_name, 'known_for_department': cast_department, 'profile_path': profile_path, 'character': cast_character})
        if 'crew' in data:
            for data_ in data['crew']:
                crew_id = data_['id']
                crew_name = data_['name']
                crew_department = data_['known_for_department']

                if crew_department == 'Directing':
                    director_crew.append(crew_name)
                
                data_crew.append({'id': crew_id, 'name': crew_name, 'department': crew_department})

        print(data_cast, data_crew)
        return data_cast, data_crew, director_crew

    except Exception as e:
        print(e)

def getMediaImages(media_id:int, media_type:str, language:str='en', get_random_backdrop:bool=False) -> list:
    URLS = {
        'image_details': f'/{media_type}/{media_id}/images?language={language}&api_key='
    }

    url_media_detail = f'{environ.get("GET_BASE_URL")}{URLS["image_details"]}{api_key}'

    try:
        response = requests.get(url=url_media_detail, headers=headers)
        response.raise_for_status()
        data = response.json()

        
        backdrop_file_paths = [item['file_path'] for item in data.get('backdrops')]
        logo_file_paths = [item['file_path'] for item in data.get('logos')]

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

    try:
        url_media_detail = f'{environ.get("GET_BASE_URL")}{URLS["media_details"]}{api_key}'
        response = requests.get(url=url_media_detail, headers=headers).json()

        random_image_path, logo_image_path = getMediaImages(media_id, media_type, get_random_backdrop=True)
        providers = getWatchProviders(media_id, media_type)
        media_credits, media_credits_crew, director = getMediaCredits(media_id, media_type)
        media_videos_pt, media_videos_en = getMediaVideos(media_id, media_type)

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
            'random_poster_path': random_image_path,
            'production_companies': [{'id': company['id'], 'logo_path': company['logo_path'], 'name': company['name'], 'origin_country': company['origin_country']} for company in response.get('production_companies', [])],
            'production_countries': [{'iso_3166_1': country['iso_3166_1'], 'name': country['name']} for country in response.get('production_countries', [])],
            'release_date': format_release_date(response.get('release_date', response.get('first_air_date'))),
            'watch_providers': providers,
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
            'credits': media_credits,
            'crew': media_credits_crew,
            'director': director,
            'video': media_videos_pt[0] if media_videos_pt else media_videos_en[0],
        }
        print(media_details['director'])

        return media_details

    except requests.RequestException as error:
        raise error
    except requests.HTTPError as error:
        raise error
    except Exception as e:
        raise e