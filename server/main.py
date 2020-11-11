from flask import Flask
from flask.views import MethodView
from marshmallow import Schema, fields
from flask_smorest import Api, Blueprint, abort
from marshmallow_dataclass import class_schema

from dataclasses import dataclass
from typing import List

from ..model.movie import *

app = Flask(__name__)
app.config['API_TITLE'] = 'Movies API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = '/doc'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.25.0/'
api = Api(app)


MovieSchema = class_schema(Movie)

@dataclass
class MoviesQueryArgs:
    orderby: str = None
    direction: str = None
    intersect: List[str] = None
    actor: List[str] = None
    director: List[str] = None
    writer: List[str] = None
    min_length: int = None
    max_length: int = None

MoviesQueryArgsSchema = class_schema(MoviesQueryArgs)

blp = Blueprint(
    'movies', 'movies', url_prefix='/movies',
    description='Get movies info'
)

@blp.route('/')
class Movies(MethodView):
    """Get movies list

    Return movies.
    ---
    Internal comment not meant to be exposed.
    """

    @blp.arguments(
        MoviesQueryArgsSchema,
        location='query')
    @blp.paginate()
    @blp.response(MovieSchema(many=True))
    def get(self, args, pagination_parameters):
        """List movies"""
        pagination_parameters.item_count = 0
        return [Movie("23434", "Test", 5.0, 120, [], [], [])]

api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
