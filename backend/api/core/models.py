from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator
from .validators import validate_file_sertificate, validate_file_archive
from .utils import unique_slugify


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
    slug = models.SlugField(verbose_name="ЧПУ", editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Автор",
        related_name="organization_created_by",
    )
    modified_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Изменено",
        related_name="organization_modified_by",
    )

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, f"{self.title}")
        super().save(*args, **kwargs)

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
    slug = models.SlugField(verbose_name="ЧПУ", editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Автор",
        related_name="position_created_by",
    )
    modified_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Изменено",
        related_name="position_modified_by",
    )

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, f"{self.title}")
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Passport(models.Model):
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
    slug = models.SlugField(verbose_name="ЧПУ", editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Автор",
        related_name="passport_created_by",
    )
    modified_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Изменено",
        related_name="passport_modified_by",
    )

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, f"{self.series} {self.number}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.series} {self.number}"

    class Meta:
        verbose_name = "Паспорт"
        verbose_name_plural = "Паспорта"


class INN(models.Model):
    value = models.CharField(
        max_length=12,
        validators=[
            MinLengthValidator(12),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="ИНН",
    )
    slug = models.SlugField(verbose_name="ЧПУ", editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Автор",
        related_name="inn_created_by",
    )
    modified_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Изменено",
        related_name="inn_modified_by",
    )

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, f"{self.value}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "ИНН"
        verbose_name_plural = "ИНН"


class SNILS(models.Model):
    value = models.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(11),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="СНИЛС",
    )
    slug = models.SlugField(verbose_name="ЧПУ", editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Автор",
        related_name="snils_created_by",
    )
    modified_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Изменено",
        related_name="snils_modified_by",
    )

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, f"{self.value}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "СНИЛС"
        verbose_name_plural = "СНИЛС"


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
    slug = models.SlugField(verbose_name="ЧПУ", editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Автор",
        related_name="employee_created_by",
    )
    modified_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Изменено",
        related_name="employee_modified_by",
    )

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(
                self, f"{self.surname} {self.name} {self.patronymic}"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class CertificationCenter(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(verbose_name="ЧПУ", editable=False, unique=True)
    start_date = models.DateField(verbose_name="Дата начала действия")
    end_date = models.DateField(verbose_name="Дата окончания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Автор",
        related_name="certification_center_created_by",
    )
    modified_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Изменено",
        related_name="certification_center_modified_by",
    )

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, f"{self.title}")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"


class Sertificate(models.Model):
    title = models.CharField(max_length=200, verbose_name="Имя файла")
    file = models.FileField(
        validators=[validate_file_sertificate], verbose_name="Сертификат"
    )
    slug = models.SlugField(verbose_name="ЧПУ", editable=False, unique=True)
    start_date = models.DateField(verbose_name="Дата начала действия")
    end_date = models.DateField(verbose_name="Дата окончания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Автор",
        related_name="sertificate_created_by",
    )
    modified_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Изменено",
        related_name="sertificate_modified_by",
    )

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, f"{self.title}")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"


class ElectronicDigitalSignature(models.Model):
    title = models.CharField(max_length=200, verbose_name="Имя файла")
    sertificate = models.OneToOneField(
        Sertificate,
        on_delete=models.PROTECT,
        verbose_name="Сертификат",
        null=True,
        blank=True,
    )
    archive = models.FileField(validators=[validate_file_archive], verbose_name="Архив")
    owner = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )
    certification_centerwner = models.ForeignKey(
        CertificationCenter,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Удостоверяющий центр",
    )
    start_date = models.DateField(verbose_name="Дата начала действия")
    end_date = models.DateField(verbose_name="Дата окончания")
    slug = models.SlugField(verbose_name="ЧПУ", editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Автор",
        related_name="electronic_digital_signature_created_by",
    )
    modified_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Изменено",
        related_name="electronic_digital_signature_modified_by",
    )

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, f"{self.title}")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "ЭЦП"
        verbose_name_plural = "ЭЦП"
