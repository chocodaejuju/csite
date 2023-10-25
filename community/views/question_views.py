from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..form import QuestionForm, QImageForm
from ..models import Question,SaveQ, QImage
from django.forms import modelformset_factory

@login_required(login_url='common:login')
def question_create(request):
    ImageFormSet = modelformset_factory(QImage, form=QImageForm, extra=3)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES) # 속성 값 저장되고 객체 생성
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=QImage.objects.none())
        if form.is_valid() and formset.is_valid(): # 질문의 내용이 적합한지 확인 오류 발생시 오류메시지가 저장된다.
            question = form.save(commit=False) # 임시저장
            question.author = request.user  # author 속성에 로그인 계정 저장
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                question.hide_author = True
            else:
                question.hide_author = False
            question.create_date = timezone.now() # 날짜
            question.save() # 저장
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    photo = QImage(question=question, image=image, text=texts)
                    photo.save()
            return redirect('community:index')
    else:
        form = QuestionForm()
        formset = ImageFormSet(queryset=QImage.objects.none())
    return render(request, 'community/question_form.html', {'form': form, 'formset':formset})

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('community:detail', question_id=question.id)
    ImageFormSet = modelformset_factory(QImage, form=QImageForm, extra=3)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        formset = ImageFormSet(request.POST, request.FILES, queryset=QImage.objects.filter(question=question))
        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                question.hide_author = True
            else:
                question.hide_author = False
            question.change_date = timezone.now()  # 수정일시 저장
            question.save()
            qImages = QImage.objects.filter(question=question)
            for images in qImages:
                images.delete()
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    if (image):
                        photo = QImage(question=question, image=image, text=texts)
                        photo.save()
            return redirect('community:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
        formset = ImageFormSet(queryset=QImage.objects.filter(question=question))
    return render(request, 'community/question_form.html', {'form': form, 'formset':formset})

@login_required(login_url = 'common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('community:detail', question_id=question.id)
    question.delete()
    return redirect('community:index')

@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('community:detail', question_id=question.id)

@login_required(login_url='common:login')
def question_save(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if(SaveQ.objects.filter(question = question)):
        messages.error(request,"이미 스크랩한 글입니다.")
    else:
        saveq = SaveQ(question=question, author=request.user)
        saveq.save()
    return redirect('community:detail', question_id=question.id)