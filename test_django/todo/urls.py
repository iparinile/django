from django.urls import path
from .views import TodoView

app_name = "todos"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('todo/', TodoView.as_view()),
]
