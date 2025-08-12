Тестовое задание на работу с Stripe API

Запуск:
Запуск через Docker: docker compose down -v && docker compose up --build

Запуск вручную:
pip install -r requirements.txt
cd Stripe
python manage.py makemigrations && python manage.py migrate
python manage.py runserver