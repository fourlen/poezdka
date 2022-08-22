from django.db import models
from django.utils.timezone import now


class Users(models.Model):
    login = models.CharField(max_length=100, blank=True, null=True, verbose_name='Логин', unique=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(max_length=500, blank=True, null=True, unique=True, verbose_name='Токен авторизации ('
                                                                                              'нужен на этапе '
                                                                                              'разработки)')
    first_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='Фамилия')
    gender = models.CharField(max_length=100, blank=True, null=True, verbose_name='Пол')
    birth = models.IntegerField(blank=True, null=True, verbose_name='Дата рождения (timestamp)')
    photo = models.ImageField(null=True, blank=True, upload_to="media/", verbose_name='Аватарка')
    is_active = models.BooleanField(blank=True, default=True, verbose_name='Статус блокировки')
    phone_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='Телефон', unique=True)
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name='Почта', unique=True)
    code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Review(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True, related_name="owner",
                              verbose_name="От кого")
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True, verbose_name="На кого")
    message = models.CharField(max_length=10000, blank=True, null=True, verbose_name='Отзыв')
    mark = models.IntegerField(blank=True, null=True, default=2, verbose_name='Оценка')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва (timestamp)')

    class Meta:
        managed = True
        db_table = 'reviews'
        verbose_name_plural = 'Отзывы'


class Questions(models.Model):
    question = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Вопрос')
    answer = models.CharField(max_length=10000, blank=True, null=True, verbose_name='Ответ')

    class Meta:
        managed = True
        db_table = 'questions'
        verbose_name_plural = 'Вопросы'


class Blog(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="media/", verbose_name='Картинка')
    text = models.CharField(max_length=10000, blank=True, null=True, verbose_name='Ответ')
    header = models.CharField(max_length=100, blank=True, null=True, verbose_name='Заголовок')

    class Meta:
        managed = True
        db_table = 'blog'
        verbose_name_plural = 'Блог'
