from django import forms
from community.models import Question, Answer, Free, Comment, Tip, TipComment,Shopping,ShoppingComment
from community.models import QImage,FreeImage,TipImage,ShopImage

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 질문 모델
        fields = ['subject', 'content']  # 제목, 내용
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 12}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class QImageForm(forms.ModelForm):
    class Meta:
        model = QImage
        fields =  ('image', 'text')
        labels = {
            'image':'이미지',
            'text' :'이미지 설명',
        }


class FreeForm(forms.ModelForm):
    class Meta:
        model = Free  # 질문 모델
        fields = ['subject', 'content']  # 제목, 내용
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 12}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class FreeImageForm(forms.ModelForm):
    class Meta:
        model = FreeImage
        fields =  ('image', 'text')
        labels = {
            'image':'이미지',
            'text' :'이미지 설명',
        }


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip  # 질문 모델
        fields = ['subject', 'content']  # 제목, 내용
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 12}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class TipCommentForm(forms.ModelForm):
    class Meta:
        model = TipComment
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class TipImageForm(forms.ModelForm):
    class Meta:
        model = TipImage
        fields =  ('image', 'text')
        labels = {
            'image':'이미지',
            'text' :'이미지 설명',
        }

class ShoppingForm(forms.ModelForm):
    class Meta:
        model = Shopping  # 질문 모델
        fields = ['name', 'content']  # 제목, 내용
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 12}),
        }
        labels = {
            'name': '제목',
            'content': '내용',
        }

class ShoppingCommentForm(forms.ModelForm):
    class Meta:
        model = ShoppingComment
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class ShopImageForm(forms.ModelForm):
    class Meta:
        model = ShopImage
        fields =  ('image', 'text')
        labels = {
            'image':'이미지',
            'text' :'이미지 설명',
        }