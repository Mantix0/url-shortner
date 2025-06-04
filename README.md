# Url shortner

**Простое web api для генерации укороченных ссылок**

## Используемые технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

## Запуск

### Запуск через docker

Поднять контейнер
```
docker-compose up --build
```

Перейти на http://localhost:8000/docs для просмотра Swagger

### Альтернативный запуск без docker

Создать Portgres бд, указать переменные среды и установить зависимости
```
pip install -r requirements.txt
```

Произвести миграции
```
alembic upgrade head
```

Запустить сервер
```
uvicorn app.main:app --port 8000
```

Перейти на http://localhost:8000/docs для просмотра Swagger

### Переменные среды (Опционально)
```dotenv
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
SECRET_KEY
```
