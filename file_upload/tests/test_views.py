import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db

def test_list_images(client, image_instance):
    """Test listing images endpoint."""
    url = reverse('image-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

def test_retrieve_image(client, image_instance):
    """Test retrieving single image endpoint."""
    url = reverse('image-detail', args=[image_instance.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['width'] == 100

def test_rotate_image(client, image_instance):
    """Test image rotation endpoint."""
    url = reverse('image-rotate', args=[image_instance.id])
    data = {'image_id': image_instance.id, 'angle': 90}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK

def test_list_pdfs(client, pdf_instance):
    """Test listing PDFs endpoint."""
    url = reverse('pdf-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

def test_retrieve_pdf(client, pdf_instance):
    """Test retrieving single PDF endpoint."""
    url = reverse('pdf-detail', args=[pdf_instance.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['num_pages'] == 10

def test_upload_image(client, base64_image):
    """Test image upload endpoint."""
    url = reverse('upload-list')
    data = {
        'file': base64_image,
        'file_type': 'image'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'width' in response.data
    assert 'height' in response.data