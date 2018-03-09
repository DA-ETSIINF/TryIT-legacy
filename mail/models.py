from django.db import models
import  datetime

# Create your models here.


class Mail(models.Model):
    title = models.CharField(max_length=250)
    subject = models.CharField(max_length=250, null=True, blank=True)
    body = models.TextField()
    attachment = models.ManyToManyField("Attachment")
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True, editable=False)

    def __str__(self):
        return self.title


class Attachment(models.Model):
    file = models.FileField(upload_to="attachment/")

    def __str__(self):
        return self.file.name