

from django.urls import path
from .views import login_view, verify_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('verify/', verify_view, name='verify'),
]
