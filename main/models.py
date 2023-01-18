from django.db import models

# Create your models here.


class Restaurant(models.Model):
    image = models.ImageField(upload_to='media', null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    rating = models.IntegerField(default=0, help_text='Указывать рейтинг в integer')
    cuisine = models.CharField(max_length=50)
    work_time = models.DateTimeField()

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Restaurant"
    
class Post(models.Model):
    title = models.CharField(max_length=70, verbose_name='Название')
    image = models.ImageField(upload_to='media', null=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    cuisine = models.ForeignKey(Restaurant, related_name='post', on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)

    TYPE = [
        ('BRK', 'Завтрак'),
        ('LUN', 'Обед'),
        ('DIN', 'Ужин'),
    ]

    type = models.CharField(choices=TYPE, max_length=3, default='BRK', verbose_name='Тип')

# class Subscription(models.Model):
#     subscribe = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)

        


    
    