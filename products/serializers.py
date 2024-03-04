from rest_framework import serializers
from .models import Category, Product, File

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'description', 'avatar')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('title', 'file')

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    # foo = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('title', 'description', 'avatar', 'categories', 'files')

    # def get_foo(self, obj):
    #     return 'Hello World %s' % obj.title
