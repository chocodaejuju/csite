from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question
import logging
logger = logging.getLogger('pybo')

def index(request): #디폴트값이 QNA게시판
    logger.info("INFO 레벨로 출력")
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    first_page = 1
    question = Question.objects.all()
    questions = question.count()
    last_page = int (questions / 10) + 1
    page_object = paginator.get_page(page)
    context = {'question_list': page_object, 'first_page': first_page,'last_page':last_page, 'page': page, 'kw': kw,
}
    return render(request, 'community/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'community/question_detail.html', context)

