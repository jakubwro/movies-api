from marshmallow_dataclass import class_schema
import requests
import json

from model import Movie

MovieSchema = class_schema(Movie)

class MoviesApi():
    def __init__(self, url):
        self.url = url

    def aslist(self, query):
        path = f"{self.url}/movies?{query}"
        print('---')
        print(path)
        print('---')
        json = requests.get(path).json()
        movies = MovieSchema(many=True).load(json)
        return movies

    def count(self, query):
        query = query.take(0)
        path = f"{self.url}/movies?{query}"
        print('---')
        print(path)
        print('---')
        return json.loads(requests.get(path).headers['X-Pagination'])["total"]
