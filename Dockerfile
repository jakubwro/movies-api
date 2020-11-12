FROM python:3.9.0-alpine3.12

WORKDIR /movies-api
COPY requirements-server.txt requirements-server.txt
RUN pip3 install -r requirements-server.txt
COPY model.py model.py
COPY server.py server.py
ENV FLASK_APP server.py
EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]