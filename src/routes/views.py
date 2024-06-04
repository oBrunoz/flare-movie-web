from src import app
from flask import render_template, stream_template
from src.api.Trending import getTrending
from src.api.Details import getMediaDetails

@app.route('/')
def index():
    trendingResponse = getTrending(media_type='all', time_window='week')

    return render_template('home.html', api=trendingResponse)

@app.route('/media/<string:media_type>/<int:media_id>', methods=['GET'])
def movie(media_type, media_id):
    mediaResponse = getMediaDetails(media_id=media_id, media_type=media_type)

    return render_template('movies/movie.html', media_metadata=mediaResponse)

@app.route('/teste')
def teste():
    return render_template('index.html')
