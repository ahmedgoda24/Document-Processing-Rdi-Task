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
    
    def validate_file(self, value: str) -> str:
        """Validate a base64 encoded file and its type."""

        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

        try:
            # Split the base64 encoded file into its header and data.
            header, file_data = value.split(";base64,", 1)

            # Decode the base64 encoded file.
            file_data = base64.b64decode(file_data)

            # Validate the file size.
            if len(file_data) > MAX_FILE_SIZE:
                raise ValidationError("File size exceeds the maximum limit of 5MB.")

            # Extract the file type from the header.
            file_type = header.split(":")[1]

            # Validate the file type.
            if self.initial_data["file_type"] == "image":
                if not file_type.startswith("image/"):
                    raise ValidationError("Invalid image file.")

                # Validate the image format.
                allowed_image_types = {"jpeg", "jpg", "png", "gif", "webp"}
                image_format = imghdr.what(None, h=file_data)
                if image_format not in allowed_image_types:
                    raise ValidationError("Unsupported image format.")
            elif self.initial_data["file_type"] == "pdf":
                if file_type != "application/pdf":
                    raise ValidationError("Invalid PDF file.")
            else:
                raise ValidationError("Unsupported file type.")

            return value

        except (TypeError, ValueError, IndexError):
            raise ValidationError("Invalid base64 file format.")


   

class RotateImageSerializer(serializers.Serializer):
    image_id = serializers.IntegerField()
    angle = serializers.IntegerField()
