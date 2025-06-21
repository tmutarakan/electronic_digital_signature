from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from core.models import TrackChanges
from apps.organizations.models import Position
from apps.employees.models import Employee
from .validators import validate_file_sertificate, validate_file_archive


class CertificationCenter(TrackChanges):
    name = models.CharField(max_length=200, verbose_name="Название")
    inn = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="ИНН",
        unique=True,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Удостоверяющий центр"
        verbose_name_plural = "Удостоверяющие центры"


class Sertificate(TrackChanges):
    filename = models.CharField(max_length=200, verbose_name="Имя файла")
    file = models.FileField(
        validators=[validate_file_sertificate], verbose_name="Сертификат",
        unique=True,
    )
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, verbose_name="Должность"
    )
    certification_center = models.ForeignKey(
        CertificationCenter,
        on_delete=models.PROTECT,
        verbose_name="Удостоверяющий центр",
    )
    start_date = models.DateField(verbose_name="Дата начала действия")
    end_date = models.DateField(verbose_name="Дата окончания")

    def __str__(self):
        return str(self.filename)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Дата начала не может быть позже даты окончания.")

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"


class ElectronicDigitalSignature(TrackChanges):
    filename = models.CharField(max_length=200, verbose_name="Имя файла")
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
        related_name="signatures",
    )
    start_date = models.DateField(verbose_name="Дата начала действия")
    end_date = models.DateField(verbose_name="Дата окончания")

    def __str__(self):
        return str(self.filename)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Дата начала не может быть позже даты окончания.")

    class Meta:
        verbose_name = "ЭЦП"
        verbose_name_plural = "ЭЦП"
