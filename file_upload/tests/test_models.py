# from django.test import TestCase
# from django.conf import settings
# from ..models import Image, PDF
# import os

# class BaseDocumentTest(TestCase):
#     def setUp(self):
#         # Ensure media directory exists
#         self.test_dir = os.path.join(settings.MEDIA_ROOT, 'test_files')
#         os.makedirs(self.test_dir, exist_ok=True)
        
#         self.test_file_path = os.path.join(self.test_dir, 'test_file.txt')
#         with open(self.test_file_path, 'w') as f:
#             f.write('test content')

#     def tearDown(self):
#         # Clean up test files
#         if os.path.exists(self.test_dir):
#             for file in os.listdir(self.test_dir):
#                 os.remove(os.path.join(self.test_dir, file))
#             os.rmdir(self.test_dir)

# class ImageModelTest(BaseDocumentTest):
#     def setUp(self):
#         super().setUp()
#         self.image = Image.objects.create(
#             file_path=self.test_file_path,
#             width=100,
#             height=100,
#             channels=3
#         )

#     def test_image_creation(self):
#         """Test image model creation and attributes"""
#         self.assertEqual(self.image.width, 100)
#         self.assertEqual(self.image.height, 100)
#         self.assertEqual(self.image.channels, 3)
#         self.assertTrue(os.path.exists(self.image.file_path))
#         self.assertTrue(str(self.image).startswith('Image '))

#     def test_image_deletion(self):
#         """Test that image file is deleted when model is deleted"""
#         file_path = self.image.file_path
#         self.image.delete()
#         self.assertFalse(os.path.exists(file_path))

# class PDFModelTest(BaseDocumentTest):
#     def setUp(self):
#         super().setUp()
#         self.pdf = PDF.objects.create(
#             file_path=self.test_file_path,
#             num_pages=10,
#             page_width=595,
#             page_height=842
#         )

#     def test_pdf_creation(self):
#         """Test PDF model creation and attributes"""
#         self.assertEqual(self.pdf.num_pages, 10)
#         self.assertEqual(self.pdf.page_width, 595)
#         self.assertEqual(self.pdf.page_height, 842)
#         self.assertTrue(os.path.exists(self.pdf.file_path))
#         self.assertTrue(str(self.pdf).startswith('PDF '))

#     def test_pdf_deletion(self):
#         """Test that PDF file is deleted when model is deleted"""
#         file_path = self.pdf.file_path
#         self.pdf.delete()
#         self.assertFalse(os.path.exists(file_path))

import pytest
import os
from ..models import Image, PDF

pytestmark = pytest.mark.django_db

def test_image_creation(image_instance):
    """Test image model creation and attributes."""
    assert image_instance.width == 100
    assert image_instance.height == 100
    assert image_instance.channels == 3
    assert os.path.exists(image_instance.file_path)
    assert str(image_instance).startswith('Image ')

def test_image_deletion(image_instance):
    """Test that image file is deleted when model is deleted."""
    file_path = image_instance.file_path
    image_instance.delete()
    assert not os.path.exists(file_path)

def test_pdf_creation(pdf_instance):
    """Test PDF model creation and attributes."""
    assert pdf_instance.num_pages == 10
    assert pdf_instance.page_width == 595
    assert pdf_instance.page_height == 842
    assert os.path.exists(pdf_instance.file_path)
    assert str(pdf_instance).startswith('PDF ')

def test_pdf_deletion(pdf_instance):
    """Test that PDF file is deleted when model is deleted."""
    file_path = pdf_instance.file_path
    pdf_instance.delete()
    assert not os.path.exists(file_path)