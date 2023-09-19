from .serializers import (
PostSerializer,
PostCreateSerializer,
PostUpdateSerializer
)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.user.pagination import CustomPagination
from rest_framework.views import APIView
from .models import Post

def is_owner(request, instance):
    return request.user == instance.author or request.user.is_staff # boolean value


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = Post.objects.all()
            return self.queryset
        else:
            return self.queryset

    def get_object(self, pk=None):
        return get_object_or_404(Post, pk=pk)

    def list(self, request):
        posts = self.serializer_class.Meta.model.objects.order_by('-id').all()
        paginator = CustomPagination()
        results = paginator.paginate_queryset(posts, request)

        posts_serializers = self.get_serializer(results, many=True)
        return paginator.get_paginated_response(posts_serializers.data)

    def create(self, request):
        post_serializer = PostCreateSerializer(data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        posts = self.get_object(pk=pk)
        post_serializer = self.serializer_class(posts)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        post = self.get_object(pk=pk)
        if not is_owner(request, post):
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if 'image' not in request.data or request.data['image'] == '':
                data = request.data.copy()
                current_image = post.image
                data['image'] = current_image

                post_serializer = PostUpdateSerializer(post, data=data)
                if post_serializer.is_valid():
                    post_serializer.save()
                    return Response({'message': 'Post updated successfully', 'data': post_serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                post_serializer = PostUpdateSerializer(post, data=request.data)
                if post_serializer.is_valid():
                    post_serializer.save()
                    return Response({'message': 'Post updated successfully', 'data': post_serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        post = self.get_object(pk=pk)
        if not is_owner(request, post):
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            post.delete()
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)

class PostLikeView(APIView):
    def post(self, request, postId):
        try:
            # post.likes += 1
            post = get_object_or_404(Post, pk=postId)
            post.likes.add(request.user)
            return Response({'message': 'Post liked successfully'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'message': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)

class PostRemoveLikeView(APIView):
    def delete(self, request, postId):
        try:
            post = get_object_or_404(Post, pk=postId)
            post.likes.remove(request.user) 
            return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'message': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)