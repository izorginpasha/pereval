# Базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только файл зависимостей для ускорения сборки
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . /app/

# Открываем нужный порт (например, 8010)
EXPOSE 8010

# Указываем команду для запуска приложения
ENTRYPOINT ["python", "src/main.py"]
