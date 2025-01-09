import pytest
import os
from PIL import Image as PILImage
from io import BytesIO
import base64
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from ..models import Image, PDF

@pytest.fixture(scope='function')
def media_root(tmpdir):
    """Create a temporary media root directory."""
    media_dir = tmpdir.mkdir('media')
    settings.MEDIA_ROOT = str(media_dir)
    yield str(media_dir)
    # Cleanup happens automatically as tmpdir is a pytest fixture

@pytest.fixture
def test_image(media_root):
    """Create a test image file and return its path."""
    image_path = os.path.join(media_root, 'test_image.jpg')
    image = PILImage.new('RGB', (100, 100), color='red')
    image.save(image_path)
    return image_path

@pytest.fixture
def test_pdf(media_root):
    """Create a test PDF file and return its path."""
    pdf_path = os.path.join(media_root, 'test.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(b'%PDF-1.4\n%TEST PDF')
    return pdf_path

@pytest.fixture
def image_instance(test_image):
    """Create and return an Image model instance."""
    return Image.objects.create(
        file_path=test_image,
        width=100,
        height=100,
        channels=3
    )

@pytest.fixture
def pdf_instance(test_pdf):
    """Create and return a PDF model instance."""
    return PDF.objects.create(
        file_path=test_pdf,
        num_pages=10,
        page_width=595,
        page_height=842
    )

@pytest.fixture
def base64_image():
    """Create and return a base64 encoded test image."""
    image = PILImage.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    return f'data:image/jpeg;base64,{image_base64}'
