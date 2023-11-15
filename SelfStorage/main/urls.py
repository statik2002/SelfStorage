from django.urls import path, include

from main import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('boxes/', views.boxes_view, name='boxes'),
    path('faq/', views.faq_view, name='faq'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('registration/', views.user_registration, name='registration')
]
