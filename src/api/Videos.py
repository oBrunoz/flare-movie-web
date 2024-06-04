from os import environ
from src.api.Config import api_key, headers, format_release_date, convert_minutes_to_hours
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
                else:
                    return None
        print(videos_pt)
        print(videos_en)
        return videos_pt, videos_en
    except Exception as e:
        print(e)