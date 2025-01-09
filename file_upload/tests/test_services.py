import pytest
import os
from ..services import DocumentService
from ..models import Image, PDF

pytestmark = pytest.mark.django_db

def test_save_base64_file(base64_image, media_root):
    """Test saving base64 encoded file."""
    file_path = DocumentService.save_base64_file(base64_image, 'image')
    assert os.path.exists(file_path)

def test_process_image(test_image):
    """Test processing an image file."""
    image = DocumentService.process_image(test_image)
    assert isinstance(image, Image)
    assert image.width == 100
    assert image.height == 100
    assert image.channels == 3

def test_rotate_image(image_instance):
    """Test image rotation."""
    rotated = DocumentService.rotate_image(image_instance.id, 90)
    assert isinstance(rotated, Image)
    assert rotated.width == 100
    assert rotated.height == 100
