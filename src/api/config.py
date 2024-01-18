from os import environ
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

load_dotenv(find_dotenv(filename='.env'))
api_key = environ.get('API_KEY')

if not api_key:
    raise ValueError('API key not found in env.')

headers = {
    'Accept': 'application/json',
    'Authorization': api_key
}

def format_release_date(release_date):
    if release_date:
        try:
            date_format = datetime.strptime(str(release_date), '%Y-%m-%d').strftime('%d/%m/%Y')
            return date_format
        except ValueError:
            return release_date

    return None

def truncate_text(text:str, max_length:int=120):
    if len(text) > max_length:
        return f'{text[:max_length]} ...'
    return text
