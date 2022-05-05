FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt src/requirements.txt
WORKDIR /src

RUN pip install --upgrade pip && \
    pip install -r requirements.txt


CMD \
    chmod 755 ./docker/wait-for-it.sh && \
    ./docker/wait-for-it.sh -t 0 db:5432 --strict -- && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python scripts/create_data_fixtures.py && \
    python scripts/create_superuser.py \
    && \
    python manage.py runserver 0.0.0.0:8000

