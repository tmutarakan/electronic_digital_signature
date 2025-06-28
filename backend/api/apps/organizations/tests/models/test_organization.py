import pytest
from apps.organizations.tests.factories import OrganizationFactory


@pytest.mark.django_db
def test_organization_creation():
    organization = OrganizationFactory()
    assert organization.pk is not None
    assert organization.name is not None
    assert organization.ogrn is not None
    assert organization.inn is not None
    assert organization.kpp is not None
    assert organization.registered_address is not None
    assert organization.created_at is not None  # поле из абстрактной модели
    assert organization.updated_at is not None  # поле из абстрактной модели
    assert organization.created_by.pk is not None  # поле из абстрактной модели
    assert organization.modified_by.pk is not None  # поле из абстрактной модели
    assert organization.slug is not None  # поле из абстрактной модели
