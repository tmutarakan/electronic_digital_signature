import factory
from faker import Faker
from apps.signatures.models import (
    CertificationCenter,
    Certificate,
    ElectronicDigitalSignature,
)
from apps.organizations.tests.factories import PositionFactory
from apps.employees.tests.factories import EmployeeFactory
from core.tests.factories import BaseAbstractModelFactory, UserFactory

fake = Faker()


class CertificationCenterFactory(BaseAbstractModelFactory):
    class Meta:
        model = CertificationCenter

    name = factory.Faker("name")
    inn = factory.LazyAttribute(
        lambda _: "".join(
            fake.random_elements(
                elements=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"),
                length=10,
            )
        )
    )
    # Поля из абстрактной модели заполнятся автоматически
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class CertificateFactory(BaseAbstractModelFactory):
    class Meta:
        model = Certificate

    file = factory.django.FileField()
    position = factory.SubFactory(PositionFactory)
    certification_center = factory.SubFactory(CertificationCenterFactory)
    start_date = factory.LazyAttribute(lambda _: fake.date())
    end_date = factory.LazyAttribute(lambda _: fake.date())
    # Поля из абстрактной модели заполнятся автоматически
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class ElectronicDigitalSignatureFactory(BaseAbstractModelFactory):
    class Meta:
        model = ElectronicDigitalSignature

    certificate = factory.SubFactory(CertificateFactory)
    archive = factory.django.FileField()
    owner = factory.SubFactory(EmployeeFactory)
    start_date = factory.LazyAttribute(lambda _: fake.date())
    end_date = factory.LazyAttribute(lambda _: fake.date())
    # Поля из абстрактной модели заполнятся автоматически
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
