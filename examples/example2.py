# What was his worst-rated movie?

from client import MoviesApi
import requests

from query import MoviesQuery
from client import MoviesApi

api = MoviesApi("http://127.0.0.1:5000")
movies = MoviesQuery(api)

query = movies.where(lambda m: "Leonardo DiCaprio" in m.actors)
query = query.orderby(lambda m: m.average_rating, 'asc')
query = query.take(1)

print(f'Count: {len(query)}')
print(f'Items: {list(query)}')



