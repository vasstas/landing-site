from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import ExpertiseCard, Service, ProtectionStandard, LegalDocument

def switch_language(request, lang_code):
    """
    Custom view to switch language and redirect to the correct homepage URL.
    Sets the language cookie to ensure persistence.
    """
    # Determine the redirect URL based on the language code
    if lang_code == 'ru':
        next_url = '/ru/'
    elif lang_code == 'el':
        next_url = '/el/'
    else:
        # Default to English (root)
        next_url = '/'
        lang_code = 'en' # Ensure we set 'en' for any unknown code

    response = HttpResponseRedirect(next_url)

    # Set the language in the session if available
    if hasattr(request, 'session'):
        request.session['_language'] = lang_code

    # Set the language cookie
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, lang_code,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )
    
    return response

def home(request):
	"""Landing page with a short mission statement."""
	expertise_cards = ExpertiseCard.objects.filter(is_active=True)
	services = Service.objects.filter(is_active=True)
	standards = ProtectionStandard.objects.filter(is_active=True)
	
	# Calculate URLs for language switcher
	# Hardcoded for the landing page to ensure correctness with prefix_default_language=False
	lang_urls = {
		'en': '/switch-lang/en/',
		'ru': '/switch-lang/ru/',
		'el': '/switch-lang/el/',
	}

	context = {
		'headline': 'Минимальный Django-сайт для VDS',
		'subline': 'Готов к деплою на 94.249.192.193 с PostgreSQL и Gunicorn.',
		'cta_label': 'Показать инструкции по деплою',
		'expertise_cards': expertise_cards,
		'services': services,
		'standards': standards,
		'lang_urls': lang_urls,
	}
	return render(request, 'pages/home.html', context)


def legal_document(request, slug):
    document = get_object_or_404(LegalDocument, slug=slug, is_active=True)
    return render(request, 'pages/legal_document.html', {'document': document})
