import pytest
from apps.signatures.tests.factories import (
    CertificationCenterFactory,
    CertificateFactory,
    ElectronicDigitalSignatureFactory,
)


@pytest.mark.django_db
def test_certification_center_creation():
    certification_center = CertificationCenterFactory()
    assert certification_center.name is not None
    assert certification_center.inn is not None
    assert certification_center.created_at is not None  # поле из абстрактной модели
    assert certification_center.updated_at is not None  # поле из абстрактной модели
    assert certification_center.created_by.pk is not None  # поле из абстрактной модели
    assert certification_center.modified_by.pk is not None  # поле из абстрактной модели
    assert certification_center.slug is not None  # поле из абстрактной модели


@pytest.mark.django_db
def test_certificate_creation():
    certificate = CertificateFactory()
    assert certificate.file is not None
    assert certificate.position is not None
    assert certificate.certification_center is not None
    assert certificate.start_date is not None
    assert certificate.end_date is not None
    assert certificate.created_at is not None  # поле из абстрактной модели
    assert certificate.updated_at is not None  # поле из абстрактной модели
    assert certificate.created_by.pk is not None  # поле из абстрактной модели
    assert certificate.modified_by.pk is not None  # поле из абстрактной модели
    assert certificate.slug is not None  # поле из абстрактной модели


@pytest.mark.django_db
def test_electronic_digital_signature_creation():
    electronic_digital_signature = ElectronicDigitalSignatureFactory()
    assert electronic_digital_signature.certificate is not None
    assert electronic_digital_signature.archive is not None
    assert electronic_digital_signature.owner is not None
    assert electronic_digital_signature.start_date is not None
    assert electronic_digital_signature.end_date is not None
    assert (
        electronic_digital_signature.created_at is not None
    )  # поле из абстрактной модели
    assert (
        electronic_digital_signature.updated_at is not None
    )  # поле из абстрактной модели
    assert (
        electronic_digital_signature.created_by.pk is not None
    )  # поле из абстрактной модели
    assert (
        electronic_digital_signature.modified_by.pk is not None
    )  # поле из абстрактной модели
    assert electronic_digital_signature.slug is not None  # поле из абстрактной модели
