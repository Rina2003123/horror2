from django.db import models

class People(models.Model):
    # Типы домов для выбора
    HOUSE_TYPE_CHOICES = [
        ('apartment', 'Квартира'),
        ('house', 'Частный дом'),
        ('cottage', 'Дача'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')

    def __str__(self):
        return self.name

class AdditionalData(models.Model):
    people = models.OneToOneField(
        People, 
        on_delete=models.CASCADE,
        related_name='additional_data',
        verbose_name='Человек'
    )
    address = models.TextField(verbose_name='Адрес')
    type_house = models.CharField(
        max_length=20,
        choices=People.HOUSE_TYPE_CHOICES,
        verbose_name='Тип жилья'
    )
    electrical_appliances = models.TextField(
        verbose_name='Бытовая техника',
        help_text='Перечислите технику через запятую'
    )

    def __str__(self):
        return f"Доп. данные для {self.people.name}"