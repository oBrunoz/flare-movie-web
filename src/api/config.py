from os import environ
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from datetime import timedelta

load_dotenv(find_dotenv(filename='.env'))
api_key = environ.get('API_KEY')

if not api_key:
    raise ValueError('API key not found in env.')

headers = {
    'Accept': 'application/json',
    'Authorization': api_key
}

def convert_minutes_to_hours(minutes:int) -> str:
    if minutes is None:
        return None
    else:
        time_delta = timedelta(minutes=minutes)
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}min"
        else:
            return f"{minutes}min"

def format_release_date(release_date) -> list:
    if release_date:
        try:
            date_format = datetime.strptime(str(release_date), '%Y-%m-%d').strftime('%d/%m/%Y')
            year_format = datetime.strptime(str(release_date), '%Y-%m-%d').strftime('%Y')
            return date_format, year_format
        except ValueError:
            return release_date

    return None

def truncate_text(text:str, max_length:int=120):
    if len(text) > max_length:
        return f'{text[:max_length]} ...'
    return text
