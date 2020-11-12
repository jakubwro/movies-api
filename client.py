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
        json = requests.get(path).json()
        movies = MovieSchema(many=True).load(json)
        return movies

    def count(self, query):
        path = f"{self.url}/movies?{query}"
        print('adf')
        return json.loads(requests.get(path).headers['X-Pagination'])["total"]
