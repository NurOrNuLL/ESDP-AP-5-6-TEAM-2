# ESDP-AP-5-6-TEAM-2

## Приложение для автоматизации работы управляющего СТО
Наше приложение предоставляет простой интерфейс для ведения отчетности по ремонтным работам авто и сотрудникам СТО

## Как запустить наш проект?
### Установка зависимостей

Установите python 3.8.10 с [офф. сайта](https://www.python.org/)

Создаем окружение и устанавливаем зависимости
```
python3.8 -m venv env

source env/bin/activate # Для Linux
source env/Scripts/activate # Для Windows

pip install -r requirements.txt
```

Установите redis с [офф. сайта](https://redis.io/)

Запускаем редис
```
sudo service redis-server start
```

В корне создаем файл: .env
```
touch .env
```

Создайте aws s3 bucket и получите ACCESS_KEY и SECRET_ACCESS_KEY на [офф. сайте](https://aws.amazon.com/)

Запустите эту команду для генерации SECRET_KEY
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Добавте в .env такие данные:
```
SECRET_KEY='...' # Вместо ... сгенерированный ранее SECRET_KEY
DEBUG=True
ALLOWED_HOST='127.0.0.1'
SQL_DATABASE='postgress'
SQL_USER='postgress'
SQL_PASSWORD='postgress'
SQL_PORT=5432
SQL_HOST='127.0.0.1'
AWS_ACCESS_KEY_ID='...' # Вместо ... ваш ACCESS_KEY
AWS_SECRET_ACCESS_KEY='...' # Вместо ... ваш SECRET_ACCESS_KEY
AWS_BUCKET_NAME='...' # Вместо ... ваше название aws s3 bucket
REDIS_HOST='0.0.0.0'
REDIS_PORT='6379'
CACHE_HOST='127.0.0.1'
```

Установите PostgreSQL с [офф. сайта](https://www.postgresql.org/download/)

Создайте базу данных и роль в postgres:
```
create database postgress;
create user postgress with password 'postgress';
grant all privileges on database postgress to postgress;
```

Запускаем проект:
```
python manage.py migrate
python createsuperuser # Создаем супер пользователя для входа в админ панель
python manage.py runserver # В первом терминале
celery -A core worker  --loglevel=info # Во втором терминале
```

- Чтобы приложение заработало необходимо создать в админ панели организацию и филиал.
- Открыть админ панель можно по url [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin/)
- Залогиньтесь ранее созданным супер пользователем
