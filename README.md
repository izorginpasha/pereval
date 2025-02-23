# Приложение pereval
##Документация API доступна по адресу http://45.143.92.70:8010/api/openapi#/
## OpenAPI JSON http://45.143.92.70:8010/openapi.json
## OpenAPI YAML: Скачайте файл openapi.yaml, сохраненный при старте приложения.

### Примеры запросов
#### GET http://45.143.92.70:8010/1

# My Awesome API

[![Build Status](https://img.shields.io/travis/username/repository.svg)](https://travis-ci.org/username/repository)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Добро пожаловать в **My Awesome API** — современное REST API, построенное с использованием **FastAPI**. Этот проект позволяет быстро получать, создавать и управлять товарами.

---

## Оглавление

- [Установка](#установка)
- [Запуск](#запуск)
- [Документация API](#документация-api)
- [Docker-образ](#docker-образ)
- [Примеры запросов](#примеры-запросов)
- [Особенности](#особенности)
- [Контакты](#контакты)
- [Лицензия](#лицензия)

---

## Установка

### Предварительные требования

- Python 3.8+
- pip

### Установка зависимостей

```bash
pip install -r requirements.txt
Запуск
Для локального запуска приложения используйте следующую команду:

bash
Копировать
Редактировать
uvicorn main:app --reload