from src import app
from flask import render_template
from src.api.config import getTrending

@app.route('/')
def index():
    trendingResponse = getTrending(media_type='all', time_window='week')

    return render_template('home.html', api=trendingResponse)