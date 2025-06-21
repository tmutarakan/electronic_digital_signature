from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from core.models import TrackChanges


class Organization(TrackChanges):
    name = models.CharField(max_length=200, verbose_name="Название")
    ogrn = models.CharField(
        max_length=13,
        validators=[
            MinLengthValidator(13),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="ОГРН",
        unique=True,
    )  # Основной государственный регистрационный номер
    inn = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="ИНН",
        unique=True,
    )  # Идентификационный номер налогоплательщика
    kpp = models.CharField(
        max_length=9,
        validators=[
            MinLengthValidator(9),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="КПП",
        unique=True,
    )  # Код причины постановки на учёт
    registered_address = models.CharField(
        max_length=200, verbose_name="Юридический адрес"
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Position(TrackChanges):
    name = models.CharField(max_length=200, verbose_name="Название")
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name="Организация"
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
        unique_together = ('name', 'organization',)
