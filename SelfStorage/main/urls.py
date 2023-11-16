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
    path('registration/', views.user_registration, name='registration'),
    path('contacts/', views.contacts, name='contacts'),
    path('law_docs/', views.law_doc, name='law_doc'),
    path('policy/', views.policy, name='policy'),
    path('tariff/', views.tariff, name='tariff'),
    path('calc/', views.calc, name='calc'),
    path('feedbacks/', views.feedbacks, name='feedbacks'),
    path('storage_list/', views.storage_list, name='storage_list'),
    path('agreement/', views.agreement, name='agreement'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('order/', views.order, name='order'),
    path('close_box/<int:box_id>', views.close_box, name='close_box'),
    path('continue_rent/', views.continue_rent, name='continue_rent'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
]
