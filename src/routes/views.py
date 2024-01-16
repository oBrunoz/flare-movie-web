from src import app
from flask import render_template, stream_template
from src.api.trending import getTrending

@app.route('/')
def index():
    trendingResponse = getTrending(media_type='all', time_window='week')

    return render_template('home.html', api=trendingResponse)

@app.route('/media/<string:media_type>/<int:media_id>', methods=['GET'])
def movie(media_type, media_id):
    print(media_type, media_id)

    return render_template('movies/movie.html')
