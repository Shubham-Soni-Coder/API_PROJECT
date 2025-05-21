from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "861e109a"

@app.route('/', methods=['GET', 'POST'])
def index():
    movie = None
    error = None
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}"
        response = requests.get(url)
        data = response.json()
        if data["Response"] == "True":
            movie = {
                'title': data['Title'],
                'year': data['Year'],
                'genre': data['Genre'],
                'plot': data['Plot'],
                'poster': data['Poster'],
                'director': data['Director'],
                'actors': data['Actors'],
                'language': data['Language'],
                'country': data['Country'],
                'awards': data['Awards'],
                'ratings': data['Ratings'],
                'rated': data['Rated'],
                'runtime': data['Runtime'],
                'imdb_id': data['imdbID']
            }
        else:
            error = "Movie not found!"
    return render_template('index.html', movie=movie, error=error)

if __name__ == '__main__':
    app.run(debug=True)