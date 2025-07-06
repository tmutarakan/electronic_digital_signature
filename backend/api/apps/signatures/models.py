from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from core.models import TrackChanges
from apps.organizations.models import Position
from apps.employees.models import Employee
from .validators import validate_file_sertificate, validate_file_archive


class CertificationCenter(TrackChanges):
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
        help_text="Введите название удостоверяющего центра",
    )
    inn = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10),
            RegexValidator(regex=r"^\d+$", message="Разрешены только цифры."),
        ],
        verbose_name="ИНН",
        unique=True,
        help_text="Введите идентификационный номер налогоплательщика удостоверяющего центра",
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Удостоверяющий центр"
        verbose_name_plural = "Удостоверяющие центры"


class Sertificate(TrackChanges):
    file = models.FileField(
        validators=[validate_file_sertificate],
        verbose_name="Сертификат",
        unique=True,
        help_text="Загрузите файл сертификата",
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        verbose_name="Должность",
        help_text="Выберите должность",
    )
    certification_center = models.ForeignKey(
        CertificationCenter,
        on_delete=models.PROTECT,
        verbose_name="Удостоверяющий центр",
        help_text="Выберите удостоверяющий центр",
    )
    start_date = models.DateField(
        verbose_name="Дата начала действия", help_text="Введите дату начала действия"
    )
    end_date = models.DateField(
        verbose_name="Дата окончания", help_text="Введите дату окончания"
    )

    def __str__(self):
        return f"{self.position.name} - {self.certification_center.name} - {self.start_date} - {self.end_date}"

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Дата начала не может быть позже даты окончания.")

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"


class ElectronicDigitalSignature(TrackChanges):
    sertificate = models.OneToOneField(
        Sertificate,
        on_delete=models.PROTECT,
        verbose_name="Сертификат",
        null=True,
        blank=True,
        help_text="Выберите сертификат",
    )
    archive = models.FileField(validators=[validate_file_archive], verbose_name="Архив")
    owner = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Владелец",
        related_name="signatures",
        help_text="Выберите владельца",
    )
    start_date = models.DateField(
        verbose_name="Дата начала действия", help_text="Введите дату начала действия"
    )
    end_date = models.DateField(
        verbose_name="Дата окончания", help_text="Введите дату окончания"
    )

    def __str__(self):
        return f"{self.owner} - {self.start_date} - {self.end_date} - {self.archive}"

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Дата начала не может быть позже даты окончания.")

    class Meta:
        verbose_name = "ЭЦП"
        verbose_name_plural = "ЭЦП"
