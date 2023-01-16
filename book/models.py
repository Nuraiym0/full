
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail


from .task import send_activation_code

class UserManager(BaseUserManager):
    
    use_in_migrations = True

    def _create(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        # self.model == User
        user:User = self.model(email=email, **kwargs)
        user.set_password(password) # хеширует пароль
        user.save(using=self._db) # сохраняем в бд
        user.create_activation_code()
        send_activation_code.delay(user.activation_code, user.email) # отправляем сообщение на почту
        return user

    def create_user(self, email, password, **kwargs):
        return self._create(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        return self._create(email, password, **kwargs)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    # username = None
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    # photo = models.ImageField(upload_to='users', null=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        import string
        code = get_random_string(length=8, allowed_chars = string.ascii_lowercase + string.ascii_uppercase)
        self.activation_code = code
        self.save()

    # def send_activation_code(self):
    #     from .tasks import send_activation_code

    #     # self.create_activation_code()
    #     # activation_link = f'http://127.0.0.1:8000/account/activate/{self.activation_code}'
    #     # message = f'Жми на кнопку и не выебывайся:\n{activation_link}'
    #     # send_mail("Activate account", message, 'admin@admin.com', recipient_list=[self.email])
    #     send_activation_code.delay()


   
    @staticmethod
    def generate_activation_code():
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        return code 

    def set_activation_code(self):
        code = self.generate_activation_code()
        if User.objects.filter(activation_code=code).exists():
            self.set_activation_code()
        else:
            self.activation_code = code
            self.save()

    
    def password_confirm(self):
        activation_url = f'http://127.0.0.1:8000/account/password_confirm/{self.activation_code}'
        message = f"""
        Do you want to change password?
        Confirm password changes: {activation_url}
        """
        send_mail("Please confirm", message, "ruslan883888@gmail.com", [self.email, ])

    def __str__(self) -> str:
        return f'{self.username} -> {self.email}'
