# Тестовое задание — Работа с Stripe API

## 📋 Описание
Проект для тестирования интеграции со **Stripe API**.

## 🚀 Запуск проекта

### 1. Запуск через Docker
```bash
docker compose down -v && docker compose up --build
```

### 2. Запуск вручную
```bash
# Установка зависимостей
pip install -r requirements.txt

# Переход в директорию с проектом
cd Stripe

# Применение миграций
python manage.py makemigrations && python manage.py migrate

# Запуск сервера
python manage.py runserver
```

## 🛠 Требования
- Python 3.10+
- Docker & Docker Compose (для контейнерного запуска)
- Аккаунт Stripe (для тестирования API)

## 📄 Переменные окружения
Перед запуском убедитесь, что созданы переменные окружения (например, в `.env`):

