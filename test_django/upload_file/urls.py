from django.urls import path
from .views import UploadFileView

app_name = "upload_file"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('upload_file', UploadFileView.as_view()),
]
