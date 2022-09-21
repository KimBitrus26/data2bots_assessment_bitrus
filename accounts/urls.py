from django.urls import path, include
from .views import UpdateUserView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path('update-user/<int:pk>/', UpdateUserView.as_view(), name='update-user'),
]
