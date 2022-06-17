FROM python:3.8

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

COPY . .
