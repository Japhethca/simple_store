FROM python:latest

WORKDIR /opt/sstore

RUN pip install pipenv

COPY ./Pipfile .

COPY ./Pipfile.lock .

RUN pipenv install

COPY . .

CMD [ "pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000" ]

