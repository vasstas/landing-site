# Landing Site

Минимальный Django-проект со стартовой страницей, подготовленный для запуска на VDS (94.249.192.193) с использованием PostgreSQL, Gunicorn и Nginx без контейнеров.

## Стек
- Django 5.1
- PostgreSQL (через `psycopg`)
- Gunicorn + Nginx
- Whitenoise для статики

## Локальный запуск
1. Создайте файл `.env` на основе `.env.example`.
2. Установите зависимости:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Примените миграции и запустите dev-сервер:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
4. Страница будет доступна на `http://127.0.0.1:8000/`.

## Переменные окружения
| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | секретный ключ Django |
| `DJANGO_DEBUG` | `True` / `False` |
| `DJANGO_ALLOWED_HOSTS` | список хостов через запятую |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | список origin'ов через запятую |
| `DATABASE_URL` | строка подключения к PostgreSQL |

## Подготовка сервера (VDS)
1. Обновите систему и установите зависимости:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3-venv python3-pip postgresql postgresql-contrib nginx -y
   ```
2. Создайте пользователя и каталог проекта:
   ```bash
   sudo adduser --system --group --home /srv/landing landing
   sudo mkdir -p /srv/landing
   sudo chown landing:landing /srv/landing
   ```
3. Настройте PostgreSQL:
   ```sql
   CREATE DATABASE landing_site;
   CREATE USER landing_user WITH PASSWORD 'your-strong-password';
   ALTER ROLE landing_user SET client_encoding TO 'UTF8';
   ALTER ROLE landing_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE landing_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE landing_site TO landing_user;
   ```
4. Склонируйте репозиторий и соберите окружение:
   ```bash
   sudo -u landing -H bash -c "cd /srv/landing && git clone <repo> . && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
   ```
5. Создайте файл `/srv/landing/.env` с боевыми значениями.
6. Выполните миграции и сбор статики:
   ```bash
   sudo -u landing -H bash -c "cd /srv/landing && .venv/bin/python manage.py migrate && .venv/bin/python manage.py collectstatic --noinput"
   ```

## Gunicorn (systemd)
`/etc/systemd/system/gunicorn-landing.service`:
```ini
[Unit]
Description=Gunicorn for landing_site
After=network.target

[Service]
User=landing
Group=landing
WorkingDirectory=/srv/landing
EnvironmentFile=/srv/landing/.env
ExecStart=/srv/landing/.venv/bin/gunicorn landing_site.wsgi:application --bind 127.0.0.1:8001
Restart=on-failure
RuntimeDirectory=gunicorn

[Install]
WantedBy=multi-user.target
```
Активируйте сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-landing
```

## Nginx
`/etc/nginx/sites-available/landing`:
```nginx
server {
    listen 80;
    server_name 94.249.192.193;

    location /static/ {
        alias /srv/landing/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
Активируйте сайт и перезапустите nginx:
```bash
sudo ln -s /etc/nginx/sites-available/landing /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Ежедневная эксплуатация
- `python manage.py createsuperuser` — создать администратора.
- `python manage.py collectstatic` — обновить статику после изменений.
- `sudo systemctl restart gunicorn-landing` — перезапустить сервис после деплоя.
