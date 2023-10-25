from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from community.models import Free, Comment, SaveFree
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..form import FreeForm, FreeImageForm
from ..form import CommentForm , FreeImage
from django.forms import modelformset_factory

def index(request): #디폴트값이 QNA게시판
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    free_list = Free.objects.order_by('-create_date')

    if kw:
        free_list = free_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(comment__content__icontains=kw) |  # 댓글 내용 검색
            Q(author__username__icontains=kw) |  # 글쓴이 검색
            Q(comment__author__username__icontains=kw)   # 댓글 글쓴이 검색
        ).distinct()
    paginator = Paginator(free_list, 10)  # 페이지당 10개씩 보여주기
    first_page = 1
    free = Free.objects.all()
    frees = free.count()
    last_page = int (frees / 10) + 1
    page_object = paginator.get_page(page)
    context = {'free_list': page_object, 'first_page': first_page,'last_page':last_page, 'page': page, 'kw': kw,
}
    return render(request, 'community/free.html', context)

def free_detail(request, free_id):
    free = get_object_or_404(Free, pk=free_id)
    context = {'free': free}
    return render(request, 'community/free_detail.html', context)

@login_required(login_url='common:login')
def free_create(request):
    ImageFormSet = modelformset_factory(FreeImage, form=FreeImageForm, extra=3)
    if request.method == 'POST':
        form = FreeForm(request.POST, request.FILES) # 속성 값 저장되고 객체 생성
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=FreeImage.objects.none())
        if form.is_valid() and formset.is_valid(): # 질문의 내용이 적합한지 확인 오류 발생시 오류메시지가 저장된다.
            free = form.save(commit=False) # 임시저장
            free.author = request.user  # author 속성에 로그인 계정 저장
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                free.hide_author = True
            else:
                free.hide_author = False
            free.create_date = timezone.now() # 날짜
            free.save() # 저장
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    photo = FreeImage(free=free, image=image, text=texts)
                    photo.save()
            return redirect('community:free')
    else:
        form = FreeForm()
        formset = ImageFormSet(queryset=FreeImage.objects.none())
    return render(request, 'community/free_form.html', {'form': form, 'formset':formset})

@login_required(login_url='common:login')
def free_modify(request, free_id):
    free = get_object_or_404(Free, pk=free_id)
    if request.user != free.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('community:free_detail', free_id=free.id)
    ImageFormSet = modelformset_factory(FreeImage, form=FreeImageForm, extra=3)
    if request.method == "POST":
        form = FreeForm(request.POST, instance=free)
        formset = ImageFormSet(request.POST, request.FILES, queryset=FreeImage.objects.filter(free=free))
        if form.is_valid() and formset.is_valid():
            free = form.save(commit=False)
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                free.hide_author = True
            else:
                free.hide_author = False
            free.change_date = timezone.now()  # 수정일시 저장
            free.save()
            fImages = FreeImage.objects.filter(free=free)
            for images in fImages:
                images.delete()
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    if (image):
                        photo = FreeImage(free=free, image=image, text=texts)
                        photo.save()
            return redirect('community:free_detail', free_id=free.id)
    else:
        form = FreeForm(instance=free)
        formset = ImageFormSet(queryset=FreeImage.objects.filter(free=free))
    return render(request, 'community/free_form.html', {'form': form, 'formset':formset})

@login_required(login_url = 'common:login')
def free_delete(request, free_id):
    free = get_object_or_404(Free, pk=free_id)
    if request.user != free.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('community:free_detail', free_id=free.id)
    free.delete()
    return redirect('community:free')

@login_required(login_url='common:login')
def free_vote(request, free_id):
    free = get_object_or_404(Free, pk=free_id)
    if request.user == free.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        free.voter.add(request.user)
    return redirect('community:free_detail', free_id=free.id)

# 댓글
@login_required(login_url='common:login')
def comment_create(request, free_id):
    free = get_object_or_404(Free, pk=free_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # author 속성에 로그인 계정 저장
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                comment.hide_author = True
            else:
                comment.hide_author = False

            comment.create_date = timezone.now()
            comment.free = free
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('community:free_detail', free_id=free.id), comment.id))
    else:
        form = CommentForm()
    context = {'free': free, 'form': form}
    return render(request, 'community/free_detail.html', context)


@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('community:free_detail', free_id=comment.free.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                comment.hide_author = True
            else:
                comment.hide_author = False

            comment.change_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('community:free_detail', free_id=comment.free.id), comment.id))
    else:
        form = CommentForm(instance=comment)
        context = {'comment': comment, 'form': form}
    return render(request, 'community/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comment.delete()
    return redirect('{}#comment_{}'.format(
        resolve_url('community:free_detail', free_id= comment.free.id), comment.id))

@login_required(login_url='common:login')
def comment_vote(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, '본인이 작성한 댓글은 추천할수 없습니다')
    else:
        comment.voter.add(request.user)
    return redirect('community:free_detail', free_id=comment.free.id)

@login_required(login_url='common:login')
def free_save(request, free_id):
    free = get_object_or_404(Free, pk=free_id)
    if(SaveFree.objects.filter(free = free)):
        messages.error(request,"이미 스크랩한 글입니다.")
    else:
        saveq = SaveFree(free=free, author=request.user)
        saveq.save()
    return redirect('community:free_detail', free_id=free.id)