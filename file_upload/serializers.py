# apps/documents/serializers.py
import base64
import imghdr
import os
from django.core.exceptions import ValidationError
from rest_framework import serializers
from drf_extra_fields.fields import Base64FileField, Base64ImageField
from django.conf import settings
from .models import Image, PDF

class ImageSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    location = serializers.CharField(source='file_path')
    class Meta:
        model = Image
        fields = ['id', 'location','file_url','width', 'height', 'channels', 'uploaded_at']
        
    def get_file_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        relative_path = obj.file_path.replace('\\', '/').split('media/')[-1]
        return request.build_absolute_uri(f'{settings.MEDIA_URL}{relative_path}')

class PDFSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    location = serializers.CharField(source='file_path')
    class Meta:
        model = PDF
        fields = ['id', 'location','file_url', 'num_pages', 'page_width', 'page_height', 'uploaded_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        relative_path = obj.file_path.replace('\\', '/').split('media/')[-1]
        return request.build_absolute_uri(f'{settings.MEDIA_URL}{relative_path}')

class FileUploadSerializer(serializers.Serializer):
    file = serializers.CharField()  # Base64 encoded file
    file_type = serializers.ChoiceField(choices=['image', 'pdf'])

   

class RotateImageSerializer(serializers.Serializer):
    image_id = serializers.IntegerField()
    angle = serializers.IntegerField()
