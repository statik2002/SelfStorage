# Проект SelfStorage
Создан в образовательных целях для реализации в командном проекте на [Devman.org](http://devman.org) 


# Фаил .env
```console
SECRET_KEY=secret stroke
DEBUG=True
ALLOWED_HOSTS='127.0.0.1'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'example@gmail.com'
EMAIL_HOST_PASSWORD = 'password for application'
EMAIL_PORT = 587

REDIS_HOST = '0.0.0.0'
REDIS_PORT = '6379'
```

- запуск celery
```console
celery -A SelfStorage worker -B -l INFO
```

- запуск доккера redis
```console
docker run -d -p 6379:6379 redis
```