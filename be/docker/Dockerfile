FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

# RUN mkdir /src;
# WORKDIR /src

# # Place for Django to find the project settings from the WORKDIR
# # ENV DJANGO_SETTINGS_MODULE osoc.settings


COPY requirements.txt src/requirements.txt
WORKDIR /src

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# COPY . .


CMD \
    chmod 755 ./docker/wait-for-it.sh && \
    ./docker/wait-for-it.sh -t 0 db:5432 --strict -- && \
    # python manage.py makemigrations && \
    python manage.py migrate && \
    python scripts/create_superuser.py \
    && \
    python manage.py runserver 0.0.0.0:8000
# gunicorn osoc.wsgi -b 0.0.0.0:80 --access-logfile '-' --error-logfile '-'


