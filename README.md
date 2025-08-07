# User Segment Management API

Микросервис для управления пользователями и их сегментами с REST API на FastAPI.

## Функционал

- Создание/удаление сегментов
- Добавление/удаление пользователей в сегменты
- Автоматическое распределение сегментов по % пользователей
- Получение активных сегментов пользователя
- Документированное API (Swagger/ReDoc)

## Инструкция запуска

### Установка

```bash
git clone https://github.com/ovaam/segment-service.git
cd segment-service
```

### Создание виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск

```bash
uvicorn app.main:app --reload
```

### Документация API

После запуска станет доступен Swagger UI по адресу: http://localhost:8000/docs


# Примеры запросов

## Создание сегмента

```bash
curl -X POST "http://localhost:8000/segments/" \
-H "Content-Type: application/json" \
-d '{"slug": "MAIL_GPT", "description": "Access to GPT in emails"}'
```

## Создание пользователя

```bash
curl -X POST "http://localhost:8000/users/" \
-H "Content-Type: application/json" \
-d '{"username": "test_user", "email": "test@example.com"}'
```

## Распределение сегмента

```bash
curl -X POST "http://localhost:8000/segments/distribute/" \
-H "Content-Type: application/json" \
-d '{"slug": "MAIL_GPT", "percentage": 30}'
```

## Получение информации о пользователе

```bash
curl "http://localhost:8000/users/1"
```

# Структура проекта

```text
segment-service/
├── app/
│   ├── __init__.py
│   ├── main.py         # Основной файл приложения
│   ├── database.py     # Настройки БД
│   ├── models.py       # SQLAlchemy модели
│   ├── schemas.py      # Pydantic схемы
│   ├── crud.py         # Операции с БД
│   └── services.py     # Бизнес-логика
├── requirements.txt    # Зависимости
└── README.md 
```
