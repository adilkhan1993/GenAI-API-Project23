# GenAI API Service

## 1. Описание проекта
REST API сервис на базе FastAPI для генерации текста с использованием нейросети. Проект оборачивает модель машинного обучения в удобный веб-интерфейс и упакован в Docker для легкого развертывания.

## 2. Архитектура и технологии
* **Web Framework:** FastAPI
* **ML Model:** GPT-2 (через Hugging Face `transformers` и `torch`)
* **Сервер:** Uvicorn
* **Контейнеризация:** Docker
* **CI/CD:** GitHub Actions
* **Хостинг:** Railway

## 3. Требования к окружению
* Python 3.12+
* Docker Desktop
* Git

## 4. Переменные окружения
На данный момент сервис не требует обязательных `.env` файлов с секретными ключами (модель загружается открыто). Для CI/CD пайплайна в GitHub Secrets прописывается `RAILWAY_TOKEN`.

## 5. Инструкция по локальному запуску (без Docker)
1. Склонируйте репозиторий.
2. Создайте и активируйте виртуальное окружение: `python -m venv venv`
3. Установите зависимости: `pip install -r requirements.txt`
4. Запустите сервер: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## 6. Инструкция по запуску через Docker
1. Соберите Docker-образ: 
   `docker build -t genai-api .`
2. Запустите контейнер: 
   `docker run -p 8000:8000 genai-api`
Сервер будет доступен по адресу `http://localhost:8000`

## 7. Примеры использования API (Endpoints)
* **`GET /`** - Корневой эндпоинт, возвращает имя сервиса.
* **`GET /health`** - Проверка работоспособности сервиса (`{"status": "ok"}`).
* **`POST /generate`** - Генерация текста. 
  Пример тела запроса (JSON):
  ```json
  {
    "prompt": "Once upon a time",
    "max_tokens": 50
  }
  # GenAI API - Project 23

Это API для работы с генеративной нейросетью, написанное на FastAPI и развернутое в облаке Railway.

🚀 **Рабочий сервер (Swagger UI):** [https://friendly-vitality-production-efda.up.railway.app/docs]