from django import forms
from personal.models import note, NoteImage, Material, MatImage
from django.forms.widgets import NumberInput


class NoteForm(forms.ModelForm):
    class Meta:
        model = note  # 질문 모델
        fields = ['subject', 'content','deadline']  # 제목, 내용
        labels = {
            'subject': '제목',
            'content': '내용',
            'deadline': '목표 날짜'
        }
        widgets = {
            'deadline': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = NoteImage
        fields =  ('image', 'text')
        labels = {
            'image':'이미지',
            'text' :'이미지 설명',
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material  # 질문 모델
        fields = ['subject', 'content']  # 제목, 내용
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class MatImageForm(forms.ModelForm):
    class Meta:
        model = MatImage
        fields =  ('image', 'text')
        labels = {
            'image':'이미지',
            'text' :'이미지 설명',
        }