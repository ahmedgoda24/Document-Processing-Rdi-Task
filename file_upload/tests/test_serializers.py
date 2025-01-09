import pytest
from ..serializers import ImageSerializer, PDFSerializer, FileUploadSerializer

pytestmark = pytest.mark.django_db

def test_image_serializer_fields(image_instance):
    """Test image serializer contains all expected fields."""
    serializer = ImageSerializer(instance=image_instance)
    assert set(serializer.data.keys()) == {
        'id', 'location', 'file_url', 'width', 'height', 'channels', 'uploaded_at'
    }

def test_pdf_serializer_fields(pdf_instance):
    """Test PDF serializer contains all expected fields."""
    serializer = PDFSerializer(instance=pdf_instance)
    assert set(serializer.data.keys()) == {
        'id', 'location', 'file_url', 'num_pages', 'page_width', 'page_height', 'uploaded_at'
    }

def test_file_upload_serializer_validation(base64_image):
    """Test file upload serializer validation."""
    data = {
        'file': base64_image,
        'file_type': 'image'
    }
    serializer = FileUploadSerializer(data=data)
    assert serializer.is_valid()

def test_file_upload_serializer_invalid_type(base64_image):
    """Test file upload serializer with invalid file type."""
    data = {
        'file': base64_image,
        'file_type': 'invalid'
    }
    serializer = FileUploadSerializer(data=data)
    assert not serializer.is_valid()