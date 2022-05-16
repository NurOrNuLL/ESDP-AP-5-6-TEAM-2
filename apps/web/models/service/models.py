from django.db import models
from .category_choices import CATEGORY_CHOICES, PRICE_CATEGORY
from django.core.validators import MinValueValidator


class Service(models.Model):
    """Услуги"""
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория работ'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    price = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Цена'
    )
    note = models.CharField(
        max_length=200, null=True,
        blank=True, verbose_name='Примечание'
    )
    price_category = models.CharField(
        max_length=100, choices=PRICE_CATEGORY,
        verbose_name='Категория цены'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name', ]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
