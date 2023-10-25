from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class note(models.Model):
    subject = models.CharField(max_length=250) #제목
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_note')
    content = models.TextField()  # 내용
    create_date = models.DateTimeField()  # 작성 날짜
    change_date = models.DateTimeField(null=True, blank=True)
    hide_author = models.BooleanField(default = False)
    finish = models.BooleanField(default = False)
    deadline = models.DateTimeField(blank=True, null=True) # 완성해야하는 날짜

class NoteImage(models.Model):
    note = models.ForeignKey(note, on_delete=models.CASCADE, null = True)
    image = models.ImageField(upload_to='note',
                              blank=True, null=True)
    text = models.TextField(blank=True, null=True)

class Material(models.Model):
    subject = models.CharField(max_length=250)  # 제목
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_material')
    content = models.TextField()  # 내용
    create_date = models.DateTimeField()  # 작성 날짜
    change_date = models.DateTimeField(null=True, blank=True)

class MatImage(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, null = True)
    image = models.ImageField(upload_to='material',
                              blank=True, null=True)
    text = models.TextField(blank=True, null=True)
