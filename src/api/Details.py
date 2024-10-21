from os import environ
from src.api.Config import api_key, headers, format_release_date, convert_minutes_to_hours
from src.api.WatchProviders import getWatchProviders
from src.api.Images import getMediaImages
from src.api.Credits import getMediaCredits
from src.api.Videos import getMediaVideos
import requests

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
        revenue_formated = '${:,.2f}'.format(response.get('revenue'))
        budget_formated = '${:,.2f}'.format(response.get('budget'))
        print("AAAAAAAAAAAAA: ", director)
        media_details = {
            'adult': response.get('adult', False),
            'backdrop_path': response.get('backdrop_path', None),
            'logo_path': logo_image_path[0] if logo_image_path and len(logo_image_path) > 0 else None,
            'belongs_to_collection': response.get('belongs_to_collection', None),
            'budget': budget_formated,
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
            'revenue': revenue_formated,
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
            'video': media_videos_pt[0] if media_videos_pt else None,
        }

        return media_details

    except requests.RequestException as error:
        raise error
    except requests.HTTPError as error:
        raise error
    except Exception as e:
        raise e