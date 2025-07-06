import factory
from faker import Faker
from apps.employees.models import Employee, Passport, INN, SNILS
from core.tests.factories import BaseAbstractModelFactory, UserFactory


fake = Faker()


class PassportFactory(BaseAbstractModelFactory):
    class Meta:
        model = Passport

    series = factory.LazyAttribute(lambda _: fake.random_number(digits=4))
    number = factory.LazyAttribute(lambda _: fake.random_number(digits=6))
    date_of_issue = factory.LazyAttribute(lambda _: fake.date())
    birthdate = factory.LazyAttribute(lambda _: fake.date())
    birthplace = factory.LazyAttribute(lambda _: fake.city())
    code = factory.LazyAttribute(lambda _: fake.random_number(digits=8))
    # created_at и updated_at из абстрактной модели
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class INNFactory(BaseAbstractModelFactory):
    class Meta:
        model = INN

    value = factory.LazyAttribute(lambda _: fake.random_number(digits=10))
    # created_at и updated_at из абстрактной модели
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class SNILSFactory(BaseAbstractModelFactory):
    class Meta:
        model = SNILS

    value = factory.LazyAttribute(lambda _: fake.random_number(digits=11))
    # created_at и updated_at из абстрактной модели
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class EmployeeFactory(BaseAbstractModelFactory):
    class Meta:
        model = Employee

    surname = factory.LazyAttribute(lambda _: fake.last_name())
    name = factory.LazyAttribute(lambda _: fake.first_name())
    patronymic = factory.LazyAttribute(lambda _: fake.last_name())
    gender = factory.LazyAttribute(lambda _: fake.random_element(elements=["М", "Ж"]))
    passport = factory.SubFactory(PassportFactory)
    inn = factory.SubFactory(INNFactory)
    snils = factory.SubFactory(SNILSFactory)
    # created_at и updated_at из абстрактной модели
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
