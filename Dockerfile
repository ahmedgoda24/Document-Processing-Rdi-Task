# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY . /app/

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE myproject.settings

# Expose the port that Django will run on
EXPOSE 8000

# Run migrations, unit tests, and start the development server
CMD python manage.py makemigrations python manage.py migrate && python manage.py test && python manage.py runserver 0.0.0.0:8000
