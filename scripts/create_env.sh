cat <<EOF > /srv/landing/.env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=django-insecure-prod-key-12345
DATABASE_URL=postgres://landing_user:landing_db_password@localhost:5432/landing_site
DJANGO_ALLOWED_HOSTS=94.249.192.193,vassta.com,www.vassta.com
EOF
