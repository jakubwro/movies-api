import ast
import inspect
import requests
import json
from typing import Callable, Any, List
from dataclasses import dataclass
from marshmallow_dataclass import class_schema

from utils import format_qurery_string
from model import Movie

def _extract_lambda(f):
    source_text = inspect.getsource(f)
    source_ast = ast.parse(source_text)
    return next((node for node in ast.walk(source_ast) if isinstance(node, ast.Lambda)), None)

def _add_multi_param(params, attr, value):
    if not attr in params:
        params[attr] = []
    params[attr].append(value)

def _add_uni_param(params, attr, value):
    params[attr] = value

def _add_param(params, attr, value):
    plurals = {
        'actors': 'actor',
        'directors': 'director',
        'writers': 'writer',
        'intersect': 'intersect'
    }
    if attr in plurals:
        _add_multi_param(params, plurals[attr], value)
    else:
        _add_uni_param(params, attr, value)
        
def _eval_node(node):
    return eval(compile(ast.Expression(body=node), filename="", mode="eval"))

def _where_in(params, tree):
    value = tree.left
    attr = tree.comparators[0].attr
    _add_param(params, attr, _eval_node(value))

def _where_cmp(params, tree, prefix):
    left = tree.left
    right = tree.comparators[0]
    if isinstance(left, ast.Attribute):
        _add_param(params, f"{prefix}_{left.attr}", _eval_node(right))
    elif isinstance(right, ast.Attribute):
        _add_param(params, f"{prefix}_{right.attr}", _eval_node(left))

def _where_eq(params, tree):
    left = tree.left
    right = tree.comparators[0]
    if isinstance(left, ast.Attribute):
        _add_param(params, left.attr, _eval_node(right))
    elif isinstance(right, ast.Attribute):
        _add_param(params, right.attr, _eval_node(left))

def _where_call(params, tree):
    if tree.func.id == 'any' and tree.args[0].func.id == 'intersect':
        for arg in tree.args[0].args:
            _add_param(params, 'intersect', arg.attr)
        return

    raise NotImplementedError

def intersect(*attrs):
    pass

class MoviesQuery():
    def __init__(self, api, params = {}):
        self.api = api
        self.params = params
        self.enumerator = None
        self.length = None

    def __str__(self):
        return format_qurery_string(**self.params)

    def __iter__(self):
        self.enumerator = self.api.aslist(self)
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.enumerator):
            raise StopIteration
        
        self.index += 1
        return self.enumerator[self.index-1]

    def __len__(self):
        if self.enumerator:
            return len(self.enumerator)
        if self.length:
            return self.length
        
        return self.api.count(self)

    def where(self, filter: Callable[[Movie], bool]) -> "MoviesQuery":
        params = self.params.copy()
        lambda_ast = _extract_lambda(filter)
        tree = lambda_ast.body
        if isinstance(tree, ast.Call):
            _where_call(params, tree)
            return MoviesQuery(self.api, params)
        op = tree.ops[0]
        if isinstance(op, ast.In):
            _where_in(params, tree)
        if isinstance(op, ast.Eq):
            _where_eq(params, tree)
        if isinstance(op, ast.Gt) or isinstance(op, ast.GtE):
            _where_cmp(params, tree, 'min')
        if isinstance(op, ast.Lt) or isinstance(op, ast.LtE):
            _where_cmp(params, tree, 'max')

        return MoviesQuery(self.api, params)

    def orderby(self, selector: Callable[[Movie], Any], direction: str = 'asc') -> "MoviesQuery":
        params = self.params.copy()
        lambda_ast = _extract_lambda(selector)
        _add_uni_param(params, 'orderby', lambda_ast.body.attr)
        _add_uni_param(params, 'direction', direction)
        return MoviesQuery(self.api, params)

    def take(self, count: int) -> "MoviesQuery":
        params = self.params.copy()
        _add_uni_param(params, 'page_size', count)
        _add_uni_param(params, 'page', 1)
        return MoviesQuery(self.api, params)
