# apps/documents/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, PDFViewSet, UploadViewSet

router = DefaultRouter()
router.register(r'images', ImageViewSet)
router.register(r'pdfs', PDFViewSet)
router.register(r'upload', UploadViewSet, basename='upload')

urlpatterns = [
    path('', include(router.urls)),
]
