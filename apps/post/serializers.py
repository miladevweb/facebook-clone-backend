from .models import Post
from rest_framework import serializers
from apps.comment.serializers import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_image = serializers.ReadOnlyField(source='author.image.url')
    author_id = serializers.ReadOnlyField(source='author.id')
    likes = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_likes(self, obj):
        return [user.username for user in obj.likes.all()]

    # Env
    def get_image(self, obj):
        return obj.image.url.replace('http://localhost:8000', '')
    

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostUpdateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_image = serializers.ReadOnlyField(source='author.image.url')
    author_id = serializers.ReadOnlyField(source='author.id')
    likes = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
    def get_likes(self, obj):
            return [user.username for user in obj.likes.all()]