import factory
from faker import Faker
from apps.organizations.models import Organization, Position  # ваши модели-наследники
from core.tests.factories import BaseAbstractModelFactory, UserFactory


fake = Faker()


class OrganizationFactory(BaseAbstractModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker("name")
    ogrn = factory.LazyAttribute(
        lambda _: "".join(
            fake.random_elements(
                elements=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"),
                length=13,
            )
        )
    )
    inn = factory.LazyAttribute(
        lambda _: "".join(
            fake.random_elements(
                elements=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"),
                length=10,
            )
        )
    )
    kpp = factory.LazyAttribute(
        lambda _: "".join(
            fake.random_elements(
                elements=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"),
                length=9,
            )
        )
    )
    registered_address = factory.Faker("address")
    # Поля из абстрактной модели заполнятся автоматически
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class PositionFactory(BaseAbstractModelFactory):
    class Meta:
        model = Position

    name = factory.Faker("name")
    organization = factory.SubFactory(OrganizationFactory)
    # created_at и updated_at из абстрактной модели
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
