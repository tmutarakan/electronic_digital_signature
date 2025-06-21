from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from core.models import TrackChanges


class Passport(TrackChanges):
    series = models.CharField(
        max_length=4,
        validators=[
            MinLengthValidator(4),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="Серия",
    )
    number = models.CharField(
        max_length=6,
        validators=[
            MinLengthValidator(6),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="Номер",
    )
    date_of_issue = models.DateField(verbose_name="Дата выдачи")
    birthdate = models.DateField(verbose_name="Дата рождения")
    birthplace = models.CharField(max_length=200, verbose_name="Место рождения")
    code = models.CharField(
        max_length=7,
        validators=[
            MinLengthValidator(7),
            RegexValidator(regex=r"^\d{3}-\d{3}$", message="Формат: 000-000"),
        ],
        verbose_name="Код подразделения",
    )  # Код подразделения

    def __str__(self):
        return f"{self.series} {self.number}"

    class Meta:
        verbose_name = "Паспорт"
        verbose_name_plural = "Паспорта"
        unique_together = (
            "series",
            "number",
        )


class INN(TrackChanges):
    value = models.CharField(
        max_length=12,
        validators=[
            MinLengthValidator(12),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="ИНН",
        unique=True,
    )

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "ИНН"
        verbose_name_plural = "ИНН"


class SNILS(TrackChanges):
    value = models.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(11),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="СНИЛС",
        unique=True,
    )

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "СНИЛС"
        verbose_name_plural = "СНИЛС"


class Employee(TrackChanges):
    GENDER_CHOICES = [
        ("М", "Мужской"),
        ("Ж", "Женский"),
    ]
    surname = models.CharField(max_length=200, verbose_name="Фамилия")
    name = models.CharField(max_length=200, verbose_name="Имя")
    patronymic = models.CharField(max_length=200, verbose_name="Отчество")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    passport = models.OneToOneField(
        Passport,
        on_delete=models.PROTECT,
        verbose_name="Паспорт",
        null=True,
        blank=True,
    )
    inn = models.OneToOneField(
        INN,
        on_delete=models.PROTECT,
        verbose_name="ИНН",
        null=True,
        blank=True,
    )
    snils = models.OneToOneField(
        SNILS,
        on_delete=models.PROTECT,
        verbose_name="СНИЛС",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
