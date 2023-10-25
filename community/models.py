
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# 질문 모델
class Question(models.Model):
    subject = models.CharField(max_length=250) #제목
    content = models.TextField()               #내용
    create_date = models.DateTimeField()       #작성 날짜
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'author_question') # 작성자,계정 삭제시 작성한 글도 삭제된다.
    change_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 한 명이 여러 질문에 추천할 수 있다.
    hide_author = models.BooleanField(default = False)
    image = models.ImageField(null = True, upload_to ="", blank = True)

    def __str__(self): # 제목 표시
        return self.subject

#답변 모델
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)#답변한 질문
    content = models.TextField()    # 내용
    create_date = models.DateTimeField() #작성 날짜
    change_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')
    hide_author = models.BooleanField(default = False)

class Free(models.Model):
    subject = models.CharField(max_length=250) #제목
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_free')
    content = models.TextField()  # 내용
    create_date = models.DateTimeField()  # 작성 날짜
    change_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_free')
    hide_author = models.BooleanField(default = False)
    image = models.ImageField(null = True, upload_to ="", blank = True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    free = models.ForeignKey(Free, on_delete=models.CASCADE)#답변한 질문
    content = models.TextField()    # 내용
    create_date = models.DateTimeField() #작성 날짜
    change_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_comment')
    hide_author = models.BooleanField(default = False)

class Tip(models.Model):
    subject = models.CharField(max_length=250) #제목
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_tip')
    content = models.TextField()  # 내용
    create_date = models.DateTimeField()  # 작성 날짜
    change_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_tip')
    hide_author = models.BooleanField(default = False)
    image = models.ImageField(null = True, upload_to ="", blank = True)


class TipComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_tipcomment')
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)#답변한 질문
    content = models.TextField()    # 내용
    create_date = models.DateTimeField() #작성 날짜
    change_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_tipcomment')
    hide_author = models.BooleanField(default = False)


class Shopping(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_shopping')
    name = models.CharField(max_length=50) #쇼핑몰 이름
    content = models.TextField() #쇼핑몰 설명
    create_date = models.DateTimeField()  # 작성 날짜
    change_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_shopping')
    image = models.ImageField(null=True, upload_to="", blank=True)

class ShoppingComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_shoppingcomment')
    shop = models.ForeignKey(Shopping, on_delete=models.CASCADE)#댓글을 단 쇼핑몰 글
    content = models.TextField()  # 내용
    create_date = models.DateTimeField()  # 작성 날짜
    change_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_shoppingcomment')
    hide_author = models.BooleanField(default=False)

class SaveQ(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_saveQ')

class SaveFree(models.Model):
    free = models.ForeignKey(Free, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_savefree')

class SaveTip(models.Model):
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_savetip')

class SaveShop(models.Model):
    shop = models.ForeignKey(Shopping, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_saveshop')

class QImage(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null = True)
    image = models.ImageField(upload_to='question',
                              blank=True, null=True)
    text = models.TextField(blank=True, null=True)

class FreeImage(models.Model):
    free = models.ForeignKey(Free, on_delete=models.CASCADE, null = True)
    image = models.ImageField(upload_to='free',
                              blank=True, null=True)
    text = models.TextField(blank=True, null=True)

class TipImage(models.Model):
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE, null = True)
    image = models.ImageField(upload_to='tip',
                              blank=True, null=True)
    text = models.TextField(blank=True, null=True)

class ShopImage(models.Model):
    shop = models.ForeignKey(Shopping, on_delete=models.CASCADE, null = True)
    image = models.ImageField(upload_to='shop',
                              blank=True, null=True)
    text = models.TextField(blank=True, null=True)