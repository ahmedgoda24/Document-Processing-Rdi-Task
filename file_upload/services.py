import base64
import os
import uuid
from PIL import Image as PILImage
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import fitz 
from django.conf import settings
from .models import Image, PDF

class DocumentService:
    @staticmethod
    def save_base64_file(base64_string, file_type):
        try:
            header, file_data = base64_string.split(';base64,')
            decoded_file = base64.b64decode(file_data)
            file_extension = 'png' if file_type == 'image' else 'pdf'
            file_path = os.path.join(settings.MEDIA_ROOT, f'{file_type}s', f'{uuid.uuid4()}.{file_extension}')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(decoded_file)
            return file_path
        except Exception as e:
            raise ValueError(f"Error saving base64 file: {e}")

    @staticmethod
    def process_image(file_path):
        with PILImage.open(file_path) as img:
            return Image.objects.create(
                file_path=file_path,
                width=img.width,
                height=img.height,
                channels=len(img.getbands())
            )

     
    @staticmethod
    def rotate_image(image_id, angle):
        image = Image.objects.get(id=image_id)
        file_path = image.file_path
        with PILImage.open(file_path) as img:
            rotated = img.rotate(angle, expand=True)
            rotated.save(file_path)

        with PILImage.open(file_path) as updated_img:
            image.width = updated_img.width
            image.height = updated_img.height
            image.save()

        return image
       




    @staticmethod
    def process_pdf(file_path):
        try:
            doc = fitz.open(file_path)
            num_pages = doc.page_count
            first_page = doc[0]
            page_width, page_height = first_page.rect.width, first_page.rect.height
            
            return PDF.objects.create(
                file_path=file_path,
                num_pages=num_pages,
                page_width=page_width,
                page_height=page_height
            )
        except Exception as e:
            raise ValueError(f"Failed to process PDF: {e}")


    @staticmethod
    def convert_pdf_to_image(pdf_id):
        pdf = PDF.objects.get(id=pdf_id)
        pdf_path = pdf.file_path

        try:
            pdf_document = fitz.open(pdf_path)

            first_page = pdf_document[0]  
            pix = first_page.get_pixmap()  
            output_path = os.path.join(settings.MEDIA_ROOT, 'images', f'{uuid.uuid4()}.png')
            pix.save(output_path)
            return DocumentService.process_image(output_path)
        except Exception as e:
            raise RuntimeError(f"PDF to image conversion failed: {str(e)}")
        



