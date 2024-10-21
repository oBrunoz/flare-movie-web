from os import environ
from src.api.Config import api_key, headers, format_release_date, convert_minutes_to_hours
import requests

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
                crew_department = data_['department']
                crew_job = data_['job']

                if crew_department == 'Directing' and crew_job == 'Director':
                    director_crew.append({'name': crew_name, 'job': crew_department})
                
                # data_crew.append({'id': crew_id, 'name': crew_name, 'department': crew_department})

        print('Director crew: ', director_crew)
        return data_cast, data_crew, director_crew

    except Exception as e:
        print(e)