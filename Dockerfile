FROM python:3.9.0-alpine3.12

WORKDIR /movies-api
COPY . .

WORKDIR /movies-api/server
RUN pip3 install -r requirements.txt
ENV FLASK_APP main.py
EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]