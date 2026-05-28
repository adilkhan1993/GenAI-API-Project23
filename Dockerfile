# 1. Используем официальный легкий образ Python (версия 3.12, как у вас)
FROM python:3.12-slim

# 2. Устанавливаем утилиту curl (она нужна для HEALTHCHECK)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 3. Устанавливаем рабочую папку внутри контейнера
WORKDIR /code

# 4. Копируем файл с библиотеками (делаем это отдельным слоем для кэширования)
COPY requirements.txt .

# 5. Устанавливаем все библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем папку с нашим кодом
COPY ./app ./app

# 7. Настраиваем проверку "здоровья" сервера по требованиям ТЗ
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# 8. Команда для старта приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
