FROM python:3.10.15-alpine3.19
COPY requirements.txt /temp/requirements.txt
COPY recipe_proj /recipe_proj
WORKDIR /recipe_proj
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user