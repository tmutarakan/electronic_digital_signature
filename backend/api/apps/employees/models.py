from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from core.models import TrackChanges
from .validators import validate_birthdate


class Passport(TrackChanges):
    series = models.CharField(
        max_length=4,
        validators=[
            MinLengthValidator(4),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="Серия",
        help_text="Введите серию паспорта"
    )
    number = models.CharField(
        max_length=6,
        validators=[
            MinLengthValidator(6),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="Номер",
        help_text="Введите номер паспорта"
    )
    date_of_issue = models.DateField(
        verbose_name="Дата выдачи", help_text="Введите дату выдачи паспорта"
    )
    birthdate = models.DateField(
        verbose_name="Дата рождения", validators=[validate_birthdate], help_text="Введите дату рождения"
    )
    birthplace = models.CharField(max_length=200, verbose_name="Место рождения", help_text="Введите место рождения")
    code = models.CharField(
        max_length=7,
        validators=[
            MinLengthValidator(7),
            RegexValidator(regex=r"^\d{3}-\d{3}$", message="Формат: 000-000"),
        ],
        verbose_name="Код подразделения",
        help_text="Введите код подразделения"
    )

    def __str__(self):
        return f"{self.series} {self.number}"

    def clean(self):
        if self.birthdate > self.date_of_issue - relativedelta(years=14):
            raise ValidationError("Паспорт выдаётся с 14 лет. Не верная дата выдачи.")

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
        help_text="Введите ИНН"
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
        help_text="Введите СНИЛС"
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
    surname = models.CharField(max_length=200, verbose_name="Фамилия", help_text="Введите фамилию")
    name = models.CharField(max_length=200, verbose_name="Имя", help_text="Введите имя")
    patronymic = models.CharField(max_length=200, verbose_name="Отчество", help_text="Введите отчество")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол", help_text="Выберите пол")
    passport = models.OneToOneField(
        Passport,
        on_delete=models.PROTECT,
        verbose_name="Паспорт",
        null=True,
        blank=True,
        help_text="Выберите паспорт"
    )
    inn = models.OneToOneField(
        INN,
        on_delete=models.PROTECT,
        verbose_name="ИНН",
        null=True,
        blank=True,
        help_text="Выберите ИНН"
    )
    snils = models.OneToOneField(
        SNILS,
        on_delete=models.PROTECT,
        verbose_name="СНИЛС",
        null=True,
        blank=True,
        help_text="Выберите СНИЛС"
    )

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["surname", "name", "patronymic"]
