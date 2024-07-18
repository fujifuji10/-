from django.db import models
from django.contrib.auth.models import (
  AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=255) 
  age = models.IntegerField(null=True)
  email = models.EmailField(max_length=255, unique=True)
  is_active = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  picture = models.FileField(null=True,upload_to='picture/')
  
  objects = UserManager()
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']
  
  class Meta:
    db_table = 'users'
    
class UserActivateTokensManager(models.Manager):
  
  def activate_user_by_token(self, token): #UserActiveTokenからデータを取り出す際の定義を記載
    user_activate_token = self.filter(
      token=token,
      expired_at__gte=datetime.now() #期限が現在時刻よりも大きいものだけ取得
    ).first() #それぞれ上を満たす最初の値のみ取得
    user = user_activate_token.user
    user.is_active = True #条件に当てはまったuserはアクティベートを有効化する
    user.save()
    
class UserActivateTokens(models.Model):
  
  token = models.UUIDField(db_index=True) #検索する際にtokenを起点にしようと思うのでdb_indexを追加した
  expired_at = models.DateTimeField() 
  user = models.ForeignKey(
    'Users', on_delete=models.CASCADE
  )
  
  objects = UserActivateTokensManager()
  
  class Meta:
    db_table = 'user_activate_tokens'
    
@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs): #この引数はセットで使用
  print(str(uuid4)) #uuidでどんな値が出るか確認用
  print(datetime.now() + timedelta(days=1))
  user_activate_token = UserActivateTokens.objects.create(
    user=instance, token=str(uuid4()), expired_at=datetime.now() + timedelta(days=1),
    #user=第二引数のinstance化するという意味のinstanceを指定する
    #user=UserAictiveTokenのuserのこと
    #あとはUserAictiveTokenのtokenとexpired_atを指定する
  )
  print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')
  # 保存処理後にprintでターミナル上に登録ユーザーのtokenを表示する
  # 本当はメールでURLを送る方が良い。