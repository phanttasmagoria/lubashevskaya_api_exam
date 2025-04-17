# lubashevskaya_api_exam
# Task Management API
Простой REST API для управления задачами на базе FastAPI и SQLite.

## Описание проекта
Этот проект реализует API для создания, чтения, обновления и удаления задач (CRUD).  
Каждая задача содержит следующие поля:
- `id` — уникальный идентификатор задачи  
- `title` — заголовок задачи  
- `description` — описание задачи  
- `status` — статус задачи (например, "new", "in progress", "done")

API построено с использованием FastAPI и SQLAlchemy с SQLite в качестве базы данных.

## Зависимости
- Python 3.7+  
- fastapi  
- uvicorn  
- sqlalchemy  
- pydantic

## Установка и запуск
1. Клонируйте репозиторий или скопируйте файлы проекта.
2. Установите зависимости pip install fastapi uvicorn sqlalchemy pydantic
3. Запустите сервер uvicorn main:app --reload
   main — имя файла с кодом
4. Откройте браузер и перейдите по адресу: http://localhost:8000/docs — интерактивная документация Swagger UI.
