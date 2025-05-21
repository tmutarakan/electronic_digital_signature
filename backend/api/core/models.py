from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator


class Organization(models.Model):
    title = models.CharField(max_length=200)


class Position(models.Model):
    title = models.CharField(max_length=200)


class CivilDocument(models.Model):
    series = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()
    date_of_issue = models.DateField()
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=200)
    code = models.CharField(max_length=7, validators=[MinLengthValidator(50)])
    inn = models.CharField(max_length=200)
    snils = models.CharField(max_length=200)


class Employee(models.Model):
    surname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    patronymic = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=('М', 'Ж'))
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    civil_document = models.OneToOneField(CivilDocument, on_delete=models.PROTECT)
    slug = models.SlugField()
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"
