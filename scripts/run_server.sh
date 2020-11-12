#!/usr/bin/bash

docker stop $(docker ps -q --filter "ancestor=movies-api")
docker build -t movies-api .
docker run -d -p 5000:5000 movies-api