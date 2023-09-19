from django.urls import path
from .views import (
PostLikeView,
PostRemoveLikeView
)

urlpatterns = [
    path('like/<int:postId>/' , PostLikeView.as_view(), name='like' ),
    path('remove-like/<int:postId>/' , PostRemoveLikeView.as_view(), name='remove-like' ),
]
