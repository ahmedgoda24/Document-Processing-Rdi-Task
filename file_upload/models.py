from django.db import models
import os

class BaseDocument(models.Model):
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        super().delete(*args, **kwargs)

class Image(BaseDocument):
    width = models.IntegerField()
    height = models.IntegerField()
    channels = models.IntegerField()

    def __str__(self):
        return f"Image {self.id}"

class PDF(BaseDocument):
    num_pages = models.IntegerField()
    page_width = models.IntegerField()
    page_height = models.IntegerField()

    def __str__(self):
        return f"PDF {self.id}"
