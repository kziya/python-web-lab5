FROM python:3.11.3-slim-bullseye

RUN apt-get update
RUN apt-get install sqlite3


WORKDIR /app


COPY requirements.txt .


RUN python -m pip install -r requirements.txt


COPY . /app
EXPOSE 3000
CMD ["python", "./app/manage.py", "runserver", "0.0.0.0:8000"]