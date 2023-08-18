from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('sign_in/', views.sign_in, name='sign-in'),
    path('sign_out/', views.sign_out, name='sign-out'),
]