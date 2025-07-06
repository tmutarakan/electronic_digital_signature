import pytest
from apps.employees.tests.factories import (
    PassportFactory,
    INNFactory,
    SNILSFactory,
    EmployeeFactory,
)


@pytest.mark.django_db
def test_passport_creation():
    passport = PassportFactory()
    assert passport.series is not None
    assert passport.number is not None
    assert passport.date_of_issue is not None
    assert passport.birthdate is not None
    assert passport.birthplace is not None
    assert passport.code is not None
    assert passport.created_at is not None  # поле из абстрактной модели
    assert passport.updated_at is not None  # поле из абстрактной модели
    assert passport.created_by.pk is not None  # поле из абстрактной модели
    assert passport.modified_by.pk is not None  # поле из абстрактной модели
    assert passport.slug is not None  # поле из абстрактной модели


@pytest.mark.django_db
def test_inn_creation():
    inn = INNFactory()
    assert inn.value is not None
    assert inn.created_at is not None  # поле из абстрактной модели
    assert inn.updated_at is not None  # поле из абстрактной модели
    assert inn.created_by.pk is not None  # поле из абстрактной модели
    assert inn.modified_by.pk is not None  # поле из абстрактной модели
    assert inn.slug is not None  # поле из абстрактной модели


@pytest.mark.django_db
def test_snils_creation():
    snils = SNILSFactory()
    assert snils.value is not None
    assert snils.created_at is not None  # поле из абстрактной модели
    assert snils.updated_at is not None  # поле из абстрактной модели
    assert snils.created_by.pk is not None  # поле из абстрактной модели
    assert snils.modified_by.pk is not None  # поле из абстрактной модели
    assert snils.slug is not None  # поле из абстрактной модели


@pytest.mark.django_db
def test_employee_creation():
    employee = EmployeeFactory()
    assert employee.surname is not None
    assert employee.name is not None
    assert employee.patronymic is not None
    assert employee.gender is not None
    assert employee.passport is not None
    assert employee.inn is not None
    assert employee.snils is not None
    assert employee.created_at is not None  # поле из абстрактной модели
    assert employee.updated_at is not None  # поле из абстрактной модели
    assert employee.created_by.pk is not None  # поле из абстрактной модели
    assert employee.modified_by.pk is not None  # поле из абстрактной модели
    assert employee.slug is not None  # поле из абстрактной модели
