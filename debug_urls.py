import os
import django
from django.conf import settings
from django.urls import translate_url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'landing_site.settings')
django.setup()

print(f"From /ru/ to EN: '{translate_url('/ru/', 'en')}'")
print(f"From / to RU: '{translate_url('/', 'ru')}'")
print(f"From /el/ to EN: '{translate_url('/el/', 'en')}'")
