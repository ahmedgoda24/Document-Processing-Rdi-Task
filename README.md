# Document-Processing-Rdi-Task
This project is a Django-based application for uploading, managing, and processing images and PDFs.
It includes features like rotating images, converting PDFs to images, and managing uploaded files through RESTful API endpoints.


## Setup Instructions

### Prerequisites

- Python 3.8+
- Docker (for containerization)
- Mysql (or any preferred database)

### Installation

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
Run Locally
 **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

 **Set up the database:**

    - Ensure PostgreSQL is running and create a database for the project.

    - Update the `DATABASES` setting in `settings.py`:

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'your_db_name',
                'USER': 'your_db_user',
                'PASSWORD': 'your_db_password',
                'HOST': 'localhost',
                'PORT': '',
            }
        }
        ```

    - Run migrations:

        ```sh
        python manage.py migrate
        ```

 **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

 **Run the development server:**

    ```sh
    python manage.py runserver
    ```

### Docker Setup

    ```

 **Run the Docker container:**

    ```sh
    docker-compose up --build
    ```
## API Endpoints

### Upload Files
- **POST** `/api/upload/`
  - Upload images or PDF files using base64 encoding
  - Request Body:
    ```json
    
            {
              "file": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...",
              "file_type": "image"
            }
            or
            {
                "file": "data:application/pdf;base64,<base64-encoded-content>",
                "file_type": "pdf"
            }
    ```
  - Returns the created document object with its details

### Images
- **GET** `/api/images/`
  - List all images
- **GET** `/api/images/{id}/`
  - Retrieve specific image details
- **DELETE** `/api/images/{id}/`
  - Delete specific image
- **POST** `/api/images/{id}/rotate/`
  - Rotate an image
  - Request Body:
    ```json
    {
        "image_id": "id",
        "angle": "rotation_angle_in_degrees"
    }
    ```

### PDFs
- **GET** `/api/pdfs/`
  - List all PDFs
- **GET** `/api/pdfs/{id}/`
  - Retrieve specific PDF details
- **DELETE** `/api/pdfs/{id}/`
  - Delete specific PDF
- **POST** `/api/pdfs/{id}/convert_to_image/`
  - Convert PDF to image
  - Returns the created image object

## Usage Examples

### Upload an Image
```bash
curl -X POST http://your-domain/api/upload/ \
  -H "Content-Type: application/json" \
  -d '{
    "file": "base64_encoded_image_string",
    "file_type": "image"
  }'

[Previous sections remain the same...]

## Running Unit Tests

### Prerequisites
- Python 3.x
- Django
- pytest
- pytest-django

### Installation
```bash
pip install pytest pytest-django

To run all tests:pytest

To run specific test files:
pytest tests/test_models.py
pytest tests/test_views.py
pytest tests/test_serializers.py
pytest tests/test_services.py
