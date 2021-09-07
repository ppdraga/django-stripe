from django.db import models

# Create your models here.


class GoodItem(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Дата добавления', 
        auto_created=True,
        auto_now_add=True
    )
    title = models.CharField(verbose_name='Название', max_length=255)
    price = models.PositiveIntegerField(verbose_name='Цена', default=0)
    vendor = models.CharField(verbose_name='Поставщик', max_length=255)
    unit_of_measure = models.CharField(verbose_name='Единица измерения', max_length=30)

    def __str__(self):
        return f'{self.title}, {self.vendor}'

    class Meta:
        verbose_name='Карточка товара'
        verbose_name_plural='Товары'