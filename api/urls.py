from django.urls import path
from .views import (
    SignupView, verify_email, UploadView, ListFilesView,
    get_download_link, download_file
)
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('verify-email/<str:token>/', verify_email),
    path('login/', TokenObtainPairView.as_view()),
    path('upload/', UploadView.as_view()),
    path('list-files/', ListFilesView.as_view()),
    path('download-link/<int:pk>/', get_download_link),
    path('download-file/<str:token>/', download_file),
]
