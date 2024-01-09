from src import app
from flask import render_template
from src.api.config import apiGetTrending

@app.route('/')
def index():
    trendingResponse = apiGetTrending()
    print(trendingResponse)

    return render_template('home.html', api=trendingResponse)