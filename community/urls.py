from django.urls import path

from .views import base_views, question_views, answer_views, free_views, tip_views,shop_views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'community'
# 경로 community/
urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),
    path('<int:question_id>/',
         base_views.detail, name='detail'),


    # question_views.py
    path('question/create/',
         question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/',
         question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/',
         question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/',
         question_views.question_vote, name='question_vote'),
    path('question/save/<int:question_id>/',
         question_views.question_save, name='question_save'),

    # answer_views.py
    path('answer/create/<int:question_id>/',
         answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/',
         answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/',
         answer_views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/',
         answer_views.answer_vote, name='answer_vote'),

    # 자유 게시판
    path('free/',
         free_views.index, name = 'free'),
    path('free/<int:free_id>/',
         free_views.free_detail, name='free_detail'),

    path('free/create/',
         free_views.free_create, name='free_create'),
    path('free/modify/<int:free_id>/',
         free_views.free_modify, name='free_modify'),
    path('free/delete/<int:free_id>/',
         free_views.free_delete, name='free_delete'),
    path('free/vote/<int:free_id>/',
         free_views.free_vote, name='free_vote'),
    path('free/save/<int:free_id>/',
         free_views.free_save, name='free_save'),

    # free 글의 댓글 comment
    path('comment/create/<int:free_id>/',
         free_views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/',
         free_views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/',
         free_views.comment_delete, name='comment_delete'),
    path('comment/vote/<int:comment_id>/',
         free_views.comment_vote, name='comment_vote'),

    # 팁 게시판
    path('tip/',
         tip_views.index, name='tip'),
    path('tip/<int:tip_id>/',
         tip_views.tip_detail, name='tip_detail'),

    path('tip/create/',
         tip_views.tip_create, name='tip_create'),
    path('tip/modify/<int:tip_id>/',
         tip_views.tip_modify, name='tip_modify'),
    path('tip/delete/<int:tip_id>/',
         tip_views.tip_delete, name='tip_delete'),
    path('tip/vote/<int:tip_id>/',
         tip_views.tip_vote, name='tip_vote'),
    path('tip/save/<int:tip_id>/',
         tip_views.tip_save, name='tip_save'),

    # 팁글의 댓글 tipcomment
    path('tipcomment/create/<int:tip_id>/',
         tip_views.tipcomment_create, name='tipcomment_create'),
    path('tipcomment/modify/<int:tipcomment_id>/',
         tip_views.tipcomment_modify, name='tipcomment_modify'),
    path('tipcomment/delete/<int:tipcomment_id>/',
         tip_views.tipcomment_delete, name='tipcomment_delete'),
    path('tipcomment/vote/<int:tipcomment_id>/',
         tip_views.tipcomment_vote, name='tipcomment_vote'),

    #쇼핑몰 기록
    path('shopping/',
         shop_views.index, name='shop'),
    path('shopping/<int:shopping_id>/',
         shop_views.shopping_detail, name='shop_detail'),

    path('shopping/create/',
         shop_views.shopping_create, name='shop_create'),
    path('shopping/modify/<int:shopping_id>/',
         shop_views.shopping_modify, name='shop_modify'),
    path('shopping/delete/<int:shopping_id>/',
         shop_views.shopping_delete, name='shop_delete'),
    path('shopping/vote/<int:shopping_id>/',
         shop_views.shopping_vote, name='shop_vote'),
    path('shopping/save/<int:shopping_id>/',
         shop_views.shop_save, name='shop_save'),

    # 쇼핑몰글의 댓글 shopcomment
    path('shoppingcomment/create/<int:shopping_id>/',
         shop_views.shoppingcomment_create, name='shopcomment_create'),
    path('shoppingcomment/modify/<int:shoppingcomment_id>/',
         shop_views.shoppingcomment_modify, name='shopcomment_modify'),
    path('shoppingcomment/delete/<int:shoppingcomment_id>/',
         shop_views.shoppingcomment_delete, name='shopcomment_delete'),
    path('shoppingcomment/vote/<int:shoppingcomment_id>/',
         shop_views.shoppingcomment_vote, name='shopcomment_vote'),

]