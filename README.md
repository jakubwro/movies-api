# Example API for movies

## Run server

```
docker stop $(docker ps -q --filter "ancestor=movies-api")
docker build -t movies-api .
docker run -d -p 5000:5000 movies-api
```

Now you can browse swagger-ui docs: http://localhost:5000/doc/swagger-ui

## Run clint code

### Create `query` object

```
from query import MoviesQuery
from client import MoviesApi

api = MoviesApi("http://127.0.0.1:5000")
movies = MoviesQuery(api)
```

### Filter data

Write a filtering predicate as a lambda expression:
```
query = movies.where(lambda movie: movie.title == "Pacific Rim")
```

Constant expressions will be evaluated:
```
query = movies.where(lambda m: ' '.join(['Leonardo', 'DiCaprio']) in m.actors)
```

### Sorting

Use a selector lambda expression to sort by a attribute. Use 'asc' and 'desc' 
for choosing the direction.
```
query = query.orderby(lambda m: m.average_rating, 'asc')
```
### Limiting number items

Number of items retrieved can be limited to a specific number.

```
query = query.take(1)
```

### More sophisticated filters

You can use intersection to check if collections overlap

```
from query import intersect
query = movies.where(lambda movie: any(intersect(
                                            movie.directors,
                                            movie.writers,
                                            movie.actors)))
```

### Comparison on attribute value

Constant expressions will be evaluated as well!

```
query = movies.where(lambda movie: movie.length_in_minutes > 5 * 60)
```

### Retrieving results

Count will read total count from `X-Pagination` header to avoid loading data 
from network.

```
print(f'Count: {len(query)}')
print(f'Items: {list(query)}')
```
