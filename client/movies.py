from typing import List
from urllib.parse import quote
from dataclasses import dataclass
from marshmallow_dataclass import class_schema
import requests
import json

@dataclass
class Movie:
    id: str
    title: str
    average_rating: float
    length_in_hours: float
    directors: List[str]
    writers: List[str]
    actors: List[str]


MovieSchema = class_schema(Movie)

def format_arg(key, value):
    if value is None:
        return ""
    if isinstance(value, list):
        return "&".join([format_arg(key, v) for v in value])
    return f"{key}={quote(str(value))}"

def format_qurery_string(**kwargs):
    query = "&".join([format_arg(k, kwargs[k]) for k in kwargs if kwargs[k]])
    return query

class MoviesApi():
    def __init__(self, url):
        self.url = url

    def list(
        self, orderby: str = None,
        direction: str = None,
        intersect: List[str] = [],
        actor: List[str] = [],
        director: List[str] = [],
        writer: List[str] = [],
        page: int = None,
        page_size: int = None,
        min_length = None,
        max_length = None):

        query = format_qurery_string(
            orderby = orderby,
            direction = direction,
            intersect = intersect,
            actor = actor,
            director = director,
            writer = writer,
            page = page,
            page_size = page_size)

        path = f"{self.url}?{query}"
        # return path
        json = requests.get(path).json()
        return MovieSchema(many=True).load(json)

    def count(
        self, orderby: str = None,
        direction: str = None,
        intersect: List[str] = [],
        actor: List[str] = [],
        director: List[str] = [],
        writer: List[str] = [],
        page: int = None,
        page_size: int = None,
        min_length=None,
        max_length=None):

        query = format_qurery_string(
            orderby=orderby,
            direction=direction,
            intersect=intersect,
            actor=actor,
            director=director,
            writer=writer,
            page=page,
            page_size=page_size)

        path = f"{self.url}?{query}"
        return json.loads(requests.get(path).headers['X-Pagination'])["total"];
        
