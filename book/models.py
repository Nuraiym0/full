from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from book.tasks import send_activation_code


from .tasks import send_activation_code

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        # self.model == User
        user:User = self.model(email=email, **kwargs)
        user.set_password(password) # хеширует пароль
        user.create_activation_code()
        user.save(using=self._db) # сохраняем в бд
        send_activation_code.delay(user.email, user.activation_code)
        
        return user

    def create_user(self, email, password, **kwargs):
        return self._create(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs['is_active'] = True
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create(email, password, **kwargs)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=70)
    phone = models.CharField(max_length=13)
    balance = models.IntegerField(default=500)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, null=True)


    def likes(self):
        posts = self.posts.all()
        likes_count = 0

        for post in posts:
            likes_count += post.likes.count()
        
        return likes_count


    @property
    def rating(self):
        users = User.objects.all()
        ratings = []

        for user in users:
           ratings.append((user, user.likes()))
        ratings.sort(key=lambda x: x[1], reverse=True)
        
        for r in ratings:
            if self in r:
                return ratings.index(r) + 1


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def create_activation_code(self):
        self.activation_code = get_random_string(8, 'qwertyuiopasdfghjklzxcvbnm123456789')

   
    def password_confirm(self):
        activation_url = f'http://34.123.240.158/account/password_confirm/{self.activation_code}'
        message = f"""
        Do you want to change password?
        Confirm password changes: {activation_url}
        """
        send_mail("Please confirm", message, "ruslan883888@gmail.com", [self.email])


    def __str__(self) -> str:
        return f'{self.username} -> {self.email}'