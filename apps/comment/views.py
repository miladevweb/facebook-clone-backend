from rest_framework import viewsets
from .serializers import CommentSerializer, CommentCreateSerializer
from rest_framework.response import Response
from rest_framework import status

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.get_serializer().Meta.model.objects.all()
            return self.queryset
        else:
            return self.queryset

    def create(self, request):
        comment_serializer = CommentCreateSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)