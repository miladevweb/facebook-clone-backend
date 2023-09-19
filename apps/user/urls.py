from django.urls import path
from .views import (
SearchUserView,
UserLoggedDataView
)

urlpatterns = [
    path('users-search/', SearchUserView.as_view(), name='users-search'),
    path('user-logged/', UserLoggedDataView.as_view(), name='users-logged'),
]
