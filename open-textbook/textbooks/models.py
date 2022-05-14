from django.db import models

# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=50)
    overview = models.TextField()

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.TextField()