from django.db import models
import os
import pandas
# Create your models here.

class Document(models.Model):
    title = models.CharField(max_length = 200)
    uploadedFile = models.FileField(upload_to = "Uploaded Files/")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)

    def delete (self, *args, **kwargs):
        if os.path.isfile(self.uploadedFile.path):
            os.remove(self.uploadedFile.path)
        super(Document, self).delete(*args, **kwargs)


