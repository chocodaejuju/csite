from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from community.models import Shopping, ShoppingComment, SaveShop,ShopImage
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..form import ShoppingForm,ShopImageForm
from ..form import ShoppingCommentForm
from django.forms import modelformset_factory

def index(request): #디폴트값이 QNA게시판
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    shopping_list = Shopping.objects.order_by('-create_date')

    if kw:
        shopping_list = shopping_list.filter(
            Q(name__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(shoppingcomment__content__icontains=kw) |  # 댓글 내용 검색
            Q(author__username__icontains=kw) |  # 글쓴이 검색
            Q(shoppingcomment__author__username__icontains=kw)   # 댓글 글쓴이 검색
        ).distinct()
    paginator = Paginator(shopping_list, 10)  # 페이지당 10개씩 보여주기
    first_page = 1
    shopping = Shopping.objects.all()
    shoppings = shopping.count()
    last_page = int (shoppings / 10) + 1
    page_object = paginator.get_page(page)
    context = {'shopping_list': page_object, 'first_page': first_page,'last_page':last_page, 'page': page, 'kw': kw,
}
    return render(request, 'community/shop.html', context)

def shopping_detail(request, shopping_id):
    shopping = get_object_or_404(Shopping, pk=shopping_id)
    context = {'shopping': shopping}
    return render(request, 'community/shop_detail.html', context)

@login_required(login_url='common:login')
def shopping_create(request):
    ImageFormSet = modelformset_factory(ShopImage, form=ShopImageForm, extra=3)
    if request.method == 'POST':
        form = ShoppingForm(request.POST, request.FILES) # 속성 값 저장되고 객체 생성
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=ShopImage.objects.none())
        if form.is_valid() and formset.is_valid(): # 질문의 내용이 적합한지 확인 오류 발생시 오류메시지가 저장된다.
            shopping = form.save(commit=False) # 임시저장
            shopping.author = request.user  # author 속성에 로그인 계정 저장
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                shopping.hide_author = True
            else:
                shopping.hide_author = False
            shopping.create_date = timezone.now() # 날짜
            shopping.save() # 저장
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    photo = ShopImage(shop=shopping, image=image, text=texts)
                    photo.save()
            return redirect('community:shop')
    else:
        form = ShoppingForm()
        formset = ImageFormSet(queryset=ShopImage.objects.none())
    return render(request, 'community/shop_form.html', {'form': form, 'formset':formset})

@login_required(login_url='common:login')
def shopping_modify(request, shopping_id):
    shopping = get_object_or_404(Shopping, pk=shopping_id)
    if request.user != shopping.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('community:shop_detail',shopping_id=shopping.id)
    ImageFormSet = modelformset_factory(ShopImage, form=ShopImageForm, extra=3)
    if request.method == "POST":
        form = ShoppingForm(request.POST, instance=shopping)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ShopImage.objects.filter(shop=shopping))
        if form.is_valid() and formset.is_valid():
            shopping = form.save(commit=False)
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                shopping.hide_author = True
            else:
                shopping.hide_author = False
            shopping.change_date = timezone.now()  # 수정일시 저장
            shopping.save()
            sImages = ShopImage.objects.filter(shop=shopping)
            for images in sImages:
                images.delete()
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form['image']
                    texts = form['text']
                    if (image):
                        photo = ShopImage(shop=shopping, image=image, text=texts)
                        photo.save()
            return redirect('community:shop_detail', shopping_id=shopping.id)
    else:
        form = ShoppingForm(instance=shopping)
        formset = ImageFormSet(queryset=ShopImage.objects.filter(shop=shopping))
    return render(request, 'community/shop_form.html', {'form': form, 'formset':formset})

@login_required(login_url = 'common:login')
def shopping_delete(request, shopping_id):
    shopping = get_object_or_404(Shopping, pk=shopping_id)
    if request.user != shopping.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('community:shop_detail', shopping_id=shopping.id)
    shopping.delete()
    return redirect('community:shop')

@login_required(login_url='common:login')
def shopping_vote(request, shopping_id):
    shopping = get_object_or_404(Shopping, pk=shopping_id)
    if request.user == shopping.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        shopping.voter.add(request.user)
    return redirect('community:shop_detail', shopping_id=shopping.id)

# 댓글
@login_required(login_url='common:login')
def shoppingcomment_create(request, shopping_id):
    shopping = get_object_or_404(Shopping, pk=shopping_id)
    if request.method == "POST":
        form = ShoppingCommentForm(request.POST)
        if form.is_valid():
            shoppingcomment = form.save(commit=False)
            shoppingcomment.author = request.user  # author 속성에 로그인 계정 저장
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                shoppingcomment.hide_author = True
            else:
                shoppingcomment.hide_author = False

            shoppingcomment.create_date = timezone.now()
            shoppingcomment.shop = shopping
            shoppingcomment.save()
            return redirect('{}#shoppingcomment_{}'.format(
                resolve_url('community:shop_detail', shopping_id=shopping.id), shoppingcomment.id))
    else:
        form = ShoppingCommentForm()
    context = {'shopping': shopping, 'form': form}
    return render(request, 'community/shop_detail.html', context)


@login_required(login_url='common:login')
def shoppingcomment_modify(request, shoppingcomment_id):
    shoppingcomment = get_object_or_404(ShoppingComment, pk=shoppingcomment_id)
    if request.method == "POST":
        form = ShoppingCommentForm(request.POST, instance= shoppingcomment)
        if form.is_valid():
            shoppingcomment = form.save(commit=False)
            selected = request.POST.getlist('Check') # 익명 체크 값 저장
            if (len(selected) != 0): # 익명 체크로 했으면
                shoppingcomment.hide_author = True
            else:
                shoppingcomment.hide_author = False

            shoppingcomment.change_date = timezone.now()
            shoppingcomment.save()
            return redirect('{}#shoppingcomment_{}'.format(
                resolve_url('community:shop_detail',shopping_id= shoppingcomment.shop.id), shoppingcomment.id))
    else:
        form = ShoppingCommentForm(instance= shoppingcomment)
    context = {'shoppingcomment': shoppingcomment, 'form': form}
    return render(request, 'community/shopcomment_form.html', context)

@login_required(login_url='common:login')
def shoppingcomment_delete(request, shoppingcomment_id):
    shoppingcomment = get_object_or_404(ShoppingComment, pk=shoppingcomment_id)
    if request.user != shoppingcomment.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        shoppingcomment.delete()
    return redirect('{}#shoppingcomment_{}'.format(
        resolve_url('community:shop_detail', shopping_id= shoppingcomment.shop.id), shoppingcomment.id))

@login_required(login_url='common:login')
def shoppingcomment_vote(request, shoppingcomment_id):
    shoppingcomment = get_object_or_404(ShoppingComment, pk=shoppingcomment_id)
    if request.user == shoppingcomment.author:
        messages.error(request, '본인이 작성한 댓글은 추천할수 없습니다')
    else:
        shoppingcomment.voter.add(request.user)
    return redirect('community:shop_detail', shopping_id=shoppingcomment.shop.id)


@login_required(login_url='common:login')
def shop_save(request, shopping_id):
    shop = get_object_or_404(Shopping, pk=shopping_id)
    if(SaveShop.objects.filter(shop = shop)):
        messages.error(request,"이미 스크랩한 글입니다.")
    else:
        saveq = SaveShop(shop=shop, author=request.user)
        saveq.save()
    return redirect('community:shop_detail', shopping_id=shop.id)