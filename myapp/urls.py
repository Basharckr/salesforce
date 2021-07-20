from django.urls import path
from myapp.views import hello_world, fetch_data

urlpatterns = [
    path('', hello_world, name='hello'),
]
