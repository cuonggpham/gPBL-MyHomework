from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),

    path('view/sign-in.html', views.sign_in),

    path('view/sign-up.html', views.sign_up)
]