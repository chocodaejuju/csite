from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from cloth.urls import *

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') #폼의 입력값을 개별적으로 얻는다.
            first_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=first_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('cloth:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, '성공적으로 변경 되었습니다.')
            return redirect('cloth:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'common/change_password.html', {
        'form': form
    })

def page_not_found(request, exception):
    return render(request, 'common/404.html', {})
