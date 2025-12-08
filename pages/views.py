from django.shortcuts import render


def home(request):
	"""Landing page with a short mission statement."""
	context = {
		'headline': 'Минимальный Django-сайт для VDS',
		'subline': 'Готов к деплою на 94.249.192.193 с PostgreSQL и Gunicorn.',
		'cta_label': 'Показать инструкции по деплою',
	}
	return render(request, 'pages/home.html', context)
