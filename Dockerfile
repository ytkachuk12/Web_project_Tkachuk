FROM python:3.9

WORKDIR /flight_mate

ENV PYTHONDONTWRITEBITECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .
RUN pip install pipenv && pipenv install --system --ignore-pipfile

EXPOSE 8000


CMD ["python", "manage.py", "runserver"]

