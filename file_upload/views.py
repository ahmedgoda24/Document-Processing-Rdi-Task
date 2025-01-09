from django.shortcuts import render
from rest_framework import viewsets, status ,mixins ,generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Image, PDF
from .serializers import ImageSerializer, PDFSerializer, FileUploadSerializer, RotateImageSerializer
from .services import DocumentService
# Create your views here.
class UploadViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = FileUploadSerializer
    def create(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_type = serializer.validated_data['file_type']
            file_path = DocumentService.save_base64_file(
                serializer.validated_data['file'],
                file_type
            )
            
            try:
                if file_type == 'image':
                    document = DocumentService.process_image(file_path)
                    return Response(ImageSerializer(document, context={'request': request}).data)
                else:
                    document = DocumentService.process_pdf(file_path)
                    return Response(PDFSerializer(document, context={'request': request}).data)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSet(mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def rotate(self, request, pk=None):
        serializer = RotateImageSerializer(data=request.data)
        if serializer.is_valid():
            try:
                image = DocumentService.rotate_image(
                    serializer.validated_data['image_id'],
                    serializer.validated_data['angle']
                )
                return Response(ImageSerializer(image, context={'request': request}).data)
            except Image.DoesNotExist:
                return Response(
                    {'error': 'Image not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PDFViewSet(mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def convert_to_image(self, request, pk=None):
        try:
            image = DocumentService.convert_pdf_to_image(pk)
            return Response(ImageSerializer(image, context={'request': request}).data)
        except PDF.DoesNotExist:
            return Response(
                {'error': 'PDF not found'},
                status=status.HTTP_404_NOT_FOUND
            )
