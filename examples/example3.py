# What are the best-rated movies, where a single person was a writer, director, and also
# one of the actors?

from client import MoviesApi
import requests

from query import MoviesQuery, intersect
from client import MoviesApi

api = MoviesApi("http://127.0.0.1:5000")
movies = MoviesQuery(api)

query = movies.where(lambda m: any(intersect(m.directors, m.writers, m.actors)))
query = query.orderby(lambda m: m.average_rating, 'desc')

print(f'Count: {len(query)}')
print(f'Items: {list(query)}')
