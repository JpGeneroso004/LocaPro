FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependências do sistema para o psycopg2 e outras libs
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && apt-get clean

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

# O Gunicorn vai rodar a aplicação na porta 8000
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
