# How many movies are longer than five hours?

from client import MoviesApi
import requests

from query import MoviesQuery
from client import MoviesApi

api = MoviesApi("http://127.0.0.1:5000")
movies = MoviesQuery(api)

query = movies.where(lambda m: m.length_in_minutes > 5 * 60)

print(f'Count: {len(query)}')
print(f'Items: {list(query)}')
