# Используем официальный python образ
FROM python:3.11

SHELL ["/bin/bash", "-c"]

RUN pip install --upgrade pip

RUN apt update && apt install -y \
    libpq-dev \
    gcc \
    python3-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -rms /bin/bash yt

WORKDIR /yt

RUN mkdir /yt/staticfiles && mkdir /yt/static && chown -R yt:yt /yt && chmod 755 /yt

COPY --chown=yt:yt . .
RUN dos2unix /yt/manage.py && chmod +x /yt/manage.py

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

USER yt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "Stripe.wsgi:application"]


