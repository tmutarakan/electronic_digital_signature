from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, RegexValidator
from .validators import validate_file_sertificate, validate_file_archive


class Organization(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    ogrn = models.CharField(
        max_length=13,
        validators=[
            MinLengthValidator(13),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="ОГРН",
    )  # Основной государственный регистрационный номер
    inn = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="ИНН",
    )  # Идентификационный номер налогоплательщика
    kpp = models.CharField(
        max_length=9,
        validators=[
            MinLengthValidator(9),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="КПП",
    )  # Код причины постановки на учёт
    registered_address = models.CharField(
        max_length=200, verbose_name="Юридический адрес"
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Position(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name="Организация"
    )

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
    inn = models.CharField(
        max_length=12,
        validators=[
            MinLengthValidator(12),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="ИНН",
    )
    snils = models.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(11),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="СНИЛС",
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
    surname = models.CharField(max_length=200, verbose_name="Фамилия")
    name = models.CharField(max_length=200, verbose_name="Имя")
    patronymic = models.CharField(max_length=200, verbose_name="Отчество")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, verbose_name="Должность"
    )
    civil_document = models.OneToOneField(
        CivilDocument,
        on_delete=models.PROTECT,
        verbose_name="Документы",
        null=True,
        blank=True,
    )
    slug = models.SlugField()
    created_at = models.DateField(default=timezone.now, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class ElectronicDigitalSignature(models.Model):
    title = models.CharField(max_length=200, verbose_name="Имя файла")
    sertificate = models.FileField(
        validators=[validate_file_sertificate], verbose_name="Сертификат"
    )
    archive = models.FileField(validators=[validate_file_archive], verbose_name="Архив")
    owner = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "ЭЦП"
        verbose_name_plural = "ЭЦП"
