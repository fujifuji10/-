from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password

class RegistForm(forms.ModelForm):
  username = forms.CharField(label='名前')
  age = forms.IntegerField(label='年齢', min_value=0)
  email = forms.EmailField(label='メールアドレス')
  password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
  confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput)
  
  class Meta():
    model = Users
    fields = ('username', 'age', 'email', 'password')
    
  def clean(self): #パスワードがどっちも正しいかをチェックするため
    cleand_data = super().clean()
    password = cleand_data['password']
    confirm_password = cleand_data['confirm_password']
    if password != confirm_password:
      raise forms.ValidationError('パスワードが異なります')
  
  def save(self, commit=False):
    user = super().save(commit=False)
    validate_password(self.cleaned_data['password'], user) #パスワードが正しいかどうかバリデーションを行うと言う意味
    user.set_password(self.cleaned_data['password'])
    user.save()
    return user
  
class LoginForm(forms.Form):
  email = forms.CharField(label='メールアドレス')
  password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
  
class UserEditForm(forms.ModelForm):
  username = forms.CharField(label='名前')
  age = forms.IntegerField(label='年齢', min_value=0)
  email = forms.EmailField(label='メールアドレス')
  picture = forms.FileField(label='写真', required=False)
  
  class Meta:
    model = Users
    fields = ('username', 'age', 'email', 'picture') #パスワードは別の画面で更新する動きにする
    
class PasswordChangeForm(forms.ModelForm):
  password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
  confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput)
  
  class Meta():
    model = Users
    fields = ('password',)#データが1つでもタプル型として定義するために,をつける
    
  def clean(self): #パスワードがどっちも正しいかをチェックするため
    cleand_data = super().clean()
    password = cleand_data['password']
    confirm_password = cleand_data['confirm_password']
    if password != confirm_password:
      raise forms.ValidationError('パスワードが異なります')
  
  def save(self, commit=False):
    user = super().save(commit=False)
    validate_password(self.cleaned_data['password'], user) #パスワードが正しいかどうかバリデーションを行うと言う意味
    user.set_password(self.cleaned_data['password']) #user.set_password=パスワードをハッシュ化して保存するメソッド
    user.save()
    return user