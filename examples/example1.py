# How many movies did Leonardo DiCaprio star in?
from query import MoviesQuery
from client import MoviesApi

api = MoviesApi("http://127.0.0.1:5000")
movies = MoviesQuery(api)

query = movies.where(lambda movie: movie.title == "Pacific Rim")
query = movies.where(lambda movie: ' '.join(['Leonardo', 'DiCaprio']) in movie.actors)

print(f'Count: {len(query)}')
print(f'Items: {list(query)}')
