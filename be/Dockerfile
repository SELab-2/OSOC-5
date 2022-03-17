FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir /src;
WORKDIR /src

COPY ./ /src

CMD python manage.py migrate && \
    python scripts/create_superuser.py 
    # && \
    # gunicorn osoc.wsgi -b 0.0.0.0:80 --access-logfile '-' --error-logfile '-'


