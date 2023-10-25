from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from community.models import Tip, TipComment, SaveTip,TipImage
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..form import TipForm,TipImageForm
from ..form import TipCommentForm
from django.forms import modelformset_factory

def index(request): #디폴트값이 QNA게시판
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    tip_list = Tip.objects.order_by('-create_date')

    if kw:
        tip_list = tip_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(tipcomment__content__icontains=kw) |  # 댓글 내용 검색
            Q(author__username__icontains=kw) |  # 글쓴이 검색
            Q(tipcomment__author__username__icontains=kw)   # 댓글 글쓴이 검색
        ).distinct()
    paginator = Paginator(tip_list, 10)  # 페이지당 10개씩 보여주기
    first_page = 1
    tip = Tip.objects.all()
    tips = tip.count()
    last_page = int (tips / 10) + 1
    page_object = paginator.get_page(page)
    context = {'tip_list': page_object, 'first_page': first_page,'last_page':last_page, 'page': page, 'kw': kw,
}
    return render(request, 'community/tip.html', context)

def tip_detail(request, tip_id):
    tip = get_object_or_404(Tip, pk=tip_id)
    context = {'tip': tip}
    return render(request, 'community/tip_detail.html', context)

@login_required(login_url='common:login')
def tip_create(request):
    ImageFormSet = modelformset_factory(TipImage, form=TipImageForm, extra=3)
    if request.method == 'POST':
        form = TipForm(request.POST, request.FILES) # 속성 값 저장되고 객체 생성
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=TipImage.objects.none())
        if form.is_valid() and formset.is_valid(): # 질문의 내용이 적합한지 확인 오류 발생시 오류메시지가 저장된다.
            tip = form.save(commit=False) # 임시저장
            tip.author = request.user  # author 속성에 로그인 계정 저장
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                tip.hide_author = True
            else:
                tip.hide_author = False
            tip.create_date = timezone.now() # 날짜
            tip.save() # 저장
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    photo = TipImage(tip=tip, image=image, text=texts)
                    photo.save()
            return redirect('community:tip')
    else:
        form = TipForm()
        formset = ImageFormSet(queryset=TipImage.objects.none())
    return render(request, 'community/tip_form.html', {'form': form, 'formset': formset})

@login_required(login_url='common:login')
def tip_modify(request, tip_id):
    tip = get_object_or_404(Tip, pk=tip_id)
    if request.user != tip.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('community:tip_detail',tip_id=tip.id)
    ImageFormSet = modelformset_factory(TipImage, form=TipImageForm, extra=3)
    if request.method == "POST":
        form = TipForm(request.POST, instance=tip)
        formset = ImageFormSet(request.POST, request.FILES, queryset=TipImage.objects.filter(tip=tip))
        if form.is_valid()and formset.is_valid():
            tip = form.save(commit=False)
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                tip.hide_author = True
            else:
                tip.hide_author = False
            tip.change_date = timezone.now()  # 수정일시 저장
            tip.save()
            tImages = TipImage.objects.filter(tip=tip)
            for images in tImages:
                images.delete()
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    if (image):
                        photo = TipImage(tip=tip, image=image, text=texts)
                        photo.save()
            return redirect('community:tip_detail', tip_id=tip.id)
    else:
        form = TipForm(instance=tip)
        formset = ImageFormSet(queryset=TipImage.objects.filter(tip=tip))
    return render(request, 'community/tip_form.html', {'form': form, 'formset':formset})

@login_required(login_url = 'common:login')
def tip_delete(request, tip_id):
    tip = get_object_or_404(Tip, pk=tip_id)
    if request.user != tip.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('community:tip_detail', tip_id=tip.id)
    tip.delete()
    return redirect('community:tip')

@login_required(login_url='common:login')
def tip_vote(request, tip_id):
    tip = get_object_or_404(Tip, pk=tip_id)
    if request.user == tip.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        tip.voter.add(request.user)
    return redirect('community:tip_detail', tip_id=tip.id)

# 댓글
@login_required(login_url='common:login')
def tipcomment_create(request, tip_id):
    tip = get_object_or_404(Tip, pk=tip_id)
    if request.method == "POST":
        form = TipCommentForm(request.POST)
        if form.is_valid():
            tipcomment = form.save(commit=False)
            tipcomment.author = request.user  # author 속성에 로그인 계정 저장
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                tipcomment.hide_author = True
            else:
                tipcomment.hide_author = False

            tipcomment.create_date = timezone.now()
            tipcomment.tip = tip
            tipcomment.save()
            return redirect('{}#tipcomment_{}'.format(
                resolve_url('community:tip_detail', tip_id=tip.id), tipcomment.id))
    else:
        form = TipCommentForm()
    context = {'tip': tip, 'form': form}
    return render(request, 'community/tip_detail.html', context)


@login_required(login_url='common:login')
def tipcomment_modify(request, tipcomment_id):
    tipcomment = get_object_or_404(TipComment, pk=tipcomment_id)
    if request.user != tipcomment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('community:tip_detail', tip_id=tipcomment.tip.id)
    if request.method == "POST":
        form = TipCommentForm(request.POST, instance= tipcomment)
        if form.is_valid():
            tipcomment = form.save(commit=False)
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                tipcomment.hide_author = True
            else:
                tipcomment.hide_author = False

            tipcomment.change_date = timezone.now()
            tipcomment.save()
            return redirect('{}#tipcomment_{}'.format(
                resolve_url('community:tip_detail', tip_id= tipcomment.tip.id), tipcomment.id))
    else:
        form = TipCommentForm(instance= tipcomment)
    context = {'tipcomment': tipcomment, 'form': form}
    return render(request, 'community/tipcomment_form.html', context)

@login_required(login_url='common:login')
def tipcomment_delete(request, tipcomment_id):
    tipcomment = get_object_or_404(TipComment, pk=tipcomment_id)
    if request.user != tipcomment.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        tipcomment.delete()
    return redirect('{}#tipcomment_{}'.format(
        resolve_url('community:tip_detail', tip_id= tipcomment.tip.id), tipcomment.id))

@login_required(login_url='common:login')
def tipcomment_vote(request, tipcomment_id):
    tipcomment = get_object_or_404(TipComment, pk=tipcomment_id)
    if request.user == tipcomment.author:
        messages.error(request, '본인이 작성한 댓글은 추천할수 없습니다')
    else:
        tipcomment.voter.add(request.user)
    return redirect('community:tip_detail', tip_id=tipcomment.tip.id)


@login_required(login_url='common:login')
def tip_save(request, tip_id):
    tip = get_object_or_404(Tip, pk=tip_id)
    if(SaveTip.objects.filter(tip = tip)):
        messages.error(request,"이미 스크랩한 글입니다.")
    else:
        saveq = SaveTip(tip=tip, author=request.user)
        saveq.save()
    return redirect('community:tip_detail', tip_id=tip.id)