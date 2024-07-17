from django.shortcuts import render, redirect
from . import forms
from django.core.exceptions import ValidationError
from .models import UserActivateTokens
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def home(request):
  return render(
    request, 'accounts/home.html'
  )
  
def regist(request):
  regist_form = forms.RegistForm(request.POST or None)
  if regist_form.is_valid(): #下にポストして登録処理をする処理を記載↓
    try:
      regist_form.save()
      return redirect('accounts:home')
    except ValidationError as e:
      regist_form.add_error('password', e)
    # regist_form.save() #実行してもパスのバリデーション、暗号化は自動ではされない→forms.pyにsaveメソッドを追記
    
  return render(
    request, 'accounts/regist.html', context={
      'regist_form': regist_form, #登録画面を表示する処理
    }
  )
  
def activate_user(request, token): #pathを設定したactivate_userを定義しよう
#tokenを元にuser_activate_tokensをアクティベートする
  user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)
  return render(
    request, 'accounts/activate_user.html'
  )
  
def user_login(request): #まずログイン用のformを記載
  login_form = forms.LoginForm(request.POST or None)
  if login_form.is_valid():
    email = login_form.cleaned_data.get('email')
    password = login_form.cleaned_data.get('password')
    #ログイン時の2つの入力データが正しいかどうかを確認する↓
    user = authenticate(email=email, password=password)
    if user:
      if user.is_active:
        login(request, user)
        messages.success(request, 'ログイン完了しました')#ログイン成功時のメッセージ
        return redirect('accounts:home')
      else:
        messages.warning(request, 'ユーザーがアクティブではありません') #ログインに成功したがアクティブユーザーでない場合
    else:
      messages.warning(request, 'ユーザーかパスワードが間違っています') #ログイン失敗した場合
  return render(
    request, 'accounts/user_login.html', context={
      'login_form':login_form
    }
  )

@login_required #ユーザーのログイン後にしか実行できないため
def user_logout(request):
  logout(request)
  messages.success(request, 'ログアウトしました')
  return redirect('accounts:home')

@login_required
def user_edit(request):
  user_edit_form = forms.UserEditForm(request.POST or None, request.FILES or None, instance=request.user) #request.user=ログインしているユーザーインスタンスを取得することができる記載方法
  if user_edit_form.is_valid():
    messages.success(request, '更新完了しました')
    user_edit_form.save()
  return render(request, 'accounts/user_edit.html', context={
    'user_edit_form':user_edit_form
  }) #ユーザーを更新するためのviewを作成
  
@login_required
def change_password(request):
  password_change_form = forms.PasswordChangeForm(request.POST or None, instance=request.user)
  if password_change_form.is_valid():
    try:
      password_change_form.save()
      messages.success(request, 'パスワードの更新完了しました')
      #下でセッションも更新する必要があるのでインポート＋記載
      update_session_auth_hash(request, request.user) #第二引数＝ユーザー情報（認証されたユーザー情報を対象にしている）
    except ValidationError as e:
      password_change_form.add_error('password', e)
  return render(
    request, 'accounts/change_password.html', context={
      'password_change_form':password_change_form
    }
  )
      