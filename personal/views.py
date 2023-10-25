from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import NoteForm, ImageForm, MaterialForm, MatImageForm
from django.forms import modelformset_factory
from .models import note, NoteImage, Material, MatImage
from datetime import datetime, timedelta
from community.models import SaveQ, Question, SaveFree,SaveShop,SaveTip
from community.urls import *
# Create your views here.
@login_required(login_url='common:login')
def index(request):
    return render(request, 'personal/personal.html',{'user': request.user})

@login_required(login_url='common:login')
def info(request):
    return render(request, 'personal/info.html',{'user': request.user})

@login_required(login_url='common:login')
def activity(request):
    saves = SaveQ.objects.filter(author=request.user)
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    if kw:
        saves = saves.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw)   # 내용 검색
        ).distinct()
    paginator = Paginator(saves, 10)  # 페이지당 10개씩 보여주기
    first_page = 1
    saveq = saves.count()
    last_page = int(saveq / 10) + 1
    page_object = paginator.get_page(page)
    context = {'user': request.user, 'saves':page_object, 'first_page': first_page, 'last_page': last_page, 'page': page,
               'kw':kw}
    return render(request, 'personal/activity.html',context)

@login_required(login_url='common:login')
def activity_free(request):
    saves = SaveFree.objects.filter(author=request.user)
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    paginator = Paginator(saves, 10)  # 페이지당 10개씩 보여주기
    first_page = 1
    saveq = saves.count()
    last_page = int(saveq / 10) + 1
    page_object = paginator.get_page(page)
    context = {'user': request.user, 'saves':page_object, 'first_page': first_page, 'last_page': last_page, 'page': page, 'kw': kw,}
    return render(request, 'personal/activity_free.html',context)

@login_required(login_url='common:login')
def activity_tip(request):
    saves = SaveTip.objects.filter(author=request.user)
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    paginator = Paginator(saves, 10)  # 페이지당 10개씩 보여주기
    first_page = 1
    saveq = saves.count()
    last_page = int(saveq / 10) + 1
    page_object = paginator.get_page(page)
    context = {'user': request.user, 'saves':page_object, 'first_page': first_page, 'last_page': last_page, 'page': page, 'kw': kw,}
    return render(request, 'personal/activity_tip.html',context)

@login_required(login_url='common:login')
def activity_shop(request):
    saves = SaveShop.objects.filter(author=request.user)
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    paginator = Paginator(saves, 10)  # 페이지당 10개씩 보여주기
    first_page = 1
    saveq = saves.count()
    last_page = int(saveq / 10) + 1
    page_object = paginator.get_page(page)
    context = {'user': request.user, 'saves':page_object, 'first_page': first_page, 'last_page': last_page, 'page': page, 'kw': kw,}
    return render(request, 'personal/activity_shop.html',context)


def write(request):
    return render(request, 'personal/my_write.html',{'user': request.user})

def design(request):
    return render(request, 'personal/design.html',{'user': request.user})


@login_required(login_url='common:login')
def material(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    materials = Material.objects.filter(author=request.user)  # 유저가 쓴 글만
    material_list = materials.order_by('-create_date')

    if kw:
        material_list = material_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw)   # 내용 검색
        ).distinct()
    paginator = Paginator(material_list, 10)  # 페이지당 10개씩 보여주기
    first_page = 1
    material = Material.objects.all()
    materials = material.count()
    last_page = int(materials / 10) + 1
    page_object = paginator.get_page(page)
    context = {'material_list': page_object, 'first_page': first_page, 'last_page': last_page, 'page': page, 'kw': kw,
               'user': request.user }
    return render(request, 'personal/material.html',context)

def material_detail(request, material_id):
    materials = get_object_or_404(Material, pk=material_id)
    context = {'material': materials}
    return render(request, 'personal/material_detail.html', context)

@login_required(login_url='common:login')
def material_create(request):
    # 하나의 modelform 을 여러번 쓸 수 있음. 모델, 모델폼, 몇 개의 폼을 띄울건지 갯수
    ImageFormSet = modelformset_factory(MatImage, form=MatImageForm, extra=3)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES) # 속성 값 저장되고 객체 생성
        # queryset 을 none 으로 정의해서 이미지가 없어도 되도록 설정. none 은 빈 쿼리셋 리턴
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=MatImage.objects.none())
        if form.is_valid() and formset.is_valid(): # 질문의 내용이 적합한지 확인 오류 발생시 오류메시지가 저장된다.
            materials = form.save(commit=False) # 임시저장
            materials.author = request.user  # author 속성에 로그인 계정 저장
            materials.create_date = timezone.now() # 날짜
            materials.save() # 저장
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    photo = MatImage(material =materials, image=image, text = texts)
                    photo.save()
            return redirect('personal:material')
    else:
        form = MaterialForm()
        formset = ImageFormSet(queryset=MatImage.objects.none())
    return render(request, 'personal/material_form.html', {'form': form, 'formset':formset})

@login_required(login_url='common:login')
def material_modify(request, material_id):
    materials = get_object_or_404(Material, pk=material_id)
    if request.user != materials.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('personal:material_detail',note_id=materials.id)
    ImageFormSet = modelformset_factory(MatImage, form=MatImageForm, extra=3)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance = materials)  # 속성 값 저장되고 객체 생성
        # queryset 을 none 으로 정의해서 이미지가 없어도 되도록 설정. none 은 빈 쿼리셋 리턴
        formset = ImageFormSet(request.POST, request.FILES,queryset=MatImage.objects.filter(material=materials))
        if form.is_valid() and formset.is_valid():  # 질문의 내용이 적합한지 확인 오류 발생시 오류메시지가 저장된다.
            materials = form.save(commit=False)  # 임시저장
            materials.author = request.user  # author 속성에 로그인 계정 저장
            materials.change_date = timezone.now()  # 날짜
            materials.save()  # 저장
            matImages = MatImage.objects.filter(material=materials)
            for images in matImages:
                images.delete()
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    if(image):
                        photo = MatImage(material=materials, image=image, text=texts)
                        photo.save()
            return redirect('personal:material_detail', material_id=materials.id)
    else:
        form = MaterialForm(instance=materials)
        formset = ImageFormSet(queryset=MatImage.objects.filter(material = materials))
    return render(request, 'personal/material_form.html', {'form': form, 'formset': formset})

@login_required(login_url = 'common:login')
def material_delete(request, note_id):
    materials = get_object_or_404(Material, pk=note_id)
    if request.user != materials.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('personal:material_detail', material_id=materials.id)
    materials.delete()
    return redirect('personal:material')

@login_required(login_url='common:login')
def note_index(request): #디폴트값이 QNA게시판
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    key = request.POST.get('check')
    notes = note.objects.filter(author=request.user)  # 유저가 쓴 글만
    if(key == "incomplete"):
        note_list = notes.filter(finish = False)
    elif(key == "complete"):
        note_list = notes.filter(finish=True)
    elif (key == "d_day"):
        note_list = notes.exclude(deadline = None)
        note_list = note_list.order_by('deadline')
    else:
        note_list = notes.order_by('-create_date')
    if kw:
        note_list = note_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw)   # 내용 검색
        ).distinct()
    paginator = Paginator(note_list, 10)  # 페이지당 10개씩 보여주기
    first_page = 1
    note_num = note_list.count()
    last_page = int (note_num / 10) + 1
    page_object = paginator.get_page(page)
    context = {'note_list': page_object, 'first_page': first_page,'last_page':last_page, 'page': page, 'kw': kw,}
    return render(request, 'personal/note.html', context)

@login_required(login_url='common:login')
def note_detail(request, note_id):
    notes = get_object_or_404(note, pk=note_id)
    if(notes.deadline):
        today = timezone.now().date()
        end = notes.deadline.date()
        d_day = (end - today + timedelta(days=1)).days
    else:
        d_day = 0;
    context = {'note': notes, 'd_day':d_day}
    return render(request, 'personal/note_detail.html', context)

@login_required(login_url='common:login')
def note_create(request):
    # 하나의 modelform 을 여러번 쓸 수 있음. 모델, 모델폼, 몇 개의 폼을 띄울건지 갯수
    ImageFormSet = modelformset_factory(NoteImage, form=ImageForm, extra=3)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES) # 속성 값 저장되고 객체 생성
        # queryset 을 none 으로 정의해서 이미지가 없어도 되도록 설정. none 은 빈 쿼리셋 리턴
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=NoteImage.objects.none())
        if form.is_valid() and formset.is_valid(): # 질문의 내용이 적합한지 확인 오류 발생시 오류메시지가 저장된다.
            notes = form.save(commit=False) # 임시저장
            notes.author = request.user  # author 속성에 로그인 계정 저장
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 완성 체크로 했으면
                notes.finish = True
            else:
                notes.finish = False
            notes.create_date = timezone.now() # 날짜
            notes.save() # 저장
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    photo = NoteImage(note =notes, image=image, text = texts)
                    photo.save()
            return redirect('personal:note')
    else:
        form = NoteForm()
        formset = ImageFormSet(queryset=NoteImage.objects.none())
    return render(request, 'personal/note_form.html', {'form': form, 'formset':formset})

@login_required(login_url='common:login')
def note_modify(request, note_id):
    notes = get_object_or_404(note, pk=note_id)
    if request.user != notes.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('personal:note_detail',note_id=notes.id)
    ImageFormSet = modelformset_factory(NoteImage, form=ImageForm, extra=3)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance = notes)  # 속성 값 저장되고 객체 생성
        # queryset 을 none 으로 정의해서 이미지가 없어도 되도록 설정. none 은 빈 쿼리셋 리턴
        formset = ImageFormSet(request.POST, request.FILES,queryset=NoteImage.objects.filter(note=notes))
        if form.is_valid() and formset.is_valid():  # 질문의 내용이 적합한지 확인 오류 발생시 오류메시지가 저장된다.
            notes = form.save(commit=False)  # 임시저장
            notes.author = request.user  # author 속성에 로그인 계정 저장
            selected = request.POST.getlist('Check')  # 완성 체크 값 저장
            if (len(selected) != 0):  # 완성 체크로 했으면
                notes.finish = True
            else:
                notes.finish = False
            notes.change_date = timezone.now()  # 날짜
            notes.save()  # 저장
            noteImages = NoteImage.objects.filter(note=notes)
            for images in noteImages:
                images.delete()
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    if(image):
                        photo = NoteImage(note=notes, image=image, text=texts)
                        photo.save()
            return redirect('personal:note_detail', note_id=notes.id)
    else:
        form = NoteForm(instance=notes)
        formset = ImageFormSet(queryset=NoteImage.objects.filter(note = notes))
    return render(request, 'personal/note_form.html', {'form': form, 'formset': formset})

@login_required(login_url = 'common:login')
def note_delete(request, note_id):
    notes = get_object_or_404(note, pk=note_id)
    if request.user != notes.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('personal:note_detail', note_id=notes.id)
    notes.delete()
    return redirect('personal:note')


