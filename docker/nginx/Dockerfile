FROM nginx:1.25

# Удаляем дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf

# Копируем наш конфиг
COPY ./default.conf /etc/nginx/conf.d/

# Даем права
RUN chmod 644 /etc/nginx/conf.d/default.conf