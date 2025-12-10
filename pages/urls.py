from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('legal/<slug:slug>/', views.legal_document, name='legal_document'),
]
