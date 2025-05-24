from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, RegexValidator
from .validators import validate_file_sertificate, validate_file_archive


class Organization(models.Model):
    title = models.CharField(max_length=200)
    ogrn = models.CharField(
        max_length=13,
        validators=[
            MinLengthValidator(13),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
    )  # Основной государственный регистрационный номер
    inn = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
    )  # Идентификационный номер налогоплательщика
    kpp = models.CharField(
        max_length=9,
        validators=[
            MinLengthValidator(9),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
    )  # Код причины постановки на учёт
    registered_address = models.CharField(max_length=200)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Position(models.Model):
    title = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class CivilDocument(models.Model):
    series = models.CharField(
        max_length=4,
        validators=[
            MinLengthValidator(4),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
    )
    number = models.CharField(
        max_length=6,
        validators=[
            MinLengthValidator(6),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
    )
    date_of_issue = models.DateField()
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=200)
    code = models.CharField(
        max_length=7,
        validators=[
            MinLengthValidator(7),
            RegexValidator(regex=r"^\d{3}-\d{3}$", message="Формат: 000-000"),
        ],
    )  # Код подразделения
    inn = models.CharField(
        max_length=12,
        validators=[
            MinLengthValidator(12),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
    )
    snils = models.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(11),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
    )  # Страховой номер индивидуального лицевого счёта

    def __str__(self):
        return f"{self.series} {self.number}"

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class Employee(models.Model):
    GENDER_CHOICES = [
        ("М", "Мужской"),
        ("Ж", "Женский"),
    ]
    surname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    patronymic = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    civil_document = models.OneToOneField(CivilDocument, on_delete=models.PROTECT)
    slug = models.SlugField()
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class ElectronicDigitalSignature(models.Model):
    title = models.CharField(max_length=200)
    sertificate = models.FileField(validators=[validate_file_sertificate])
    archive = models.FileField(validators=[validate_file_archive])
    owner = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = "ЭЦП"
        verbose_name_plural = "ЭЦП"
