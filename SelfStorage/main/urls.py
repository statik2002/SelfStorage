from django.urls import path, include

from main import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('boxes/', views.boxes_view, name='boxes'),
    path('faq/', views.faq_view, name='faq')
]
