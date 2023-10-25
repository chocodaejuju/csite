from django import forms
from map.models import MarkerPosition


class MarkerPositionForm(forms.ModelForm):
    class Meta:
        model = MarkerPosition #사용할 모델
        fields = ['title', 'content', 'lat','lng']

