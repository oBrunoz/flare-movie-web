from src import app
from flask import render_template
from src.api.config import getTrending

@app.route('/')
def index():
    trendingResponse = getTrending()

    return render_template('home.html', api=trendingResponse)