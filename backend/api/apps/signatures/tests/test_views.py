import pytest
from django.urls import reverse
from rest_framework import status
from .factories import (
    CertificationCenterFactory,
    CertificateFactory,
    ElectronicDigitalSignatureFactory,
)

pytestmark = pytest.mark.django_db


class TestCertificationCenterCRUD:
    certification_center_list_url = reverse("signatures:certification-center-list")

    def test_create_certification_center_without_auth(self, api_client):
        data = {
            "name": "New Certification Center",
            "inn": "1234567890",
        }
        response = api_client.post(self.certification_center_list_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_certification_centers(self, api_client):
        CertificationCenterFactory.create_batch(5)
        response = api_client.get(self.certification_center_list_url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 5

    def test_delete_organization_without_auth(self, api_client):
        certification_center = CertificationCenterFactory()
        url = reverse(
            "signatures:certification-center-detail",
            kwargs={"slug": certification_center.slug},
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_certification_center_without_auth(self, api_client):
        certification_center = CertificationCenterFactory()
        data = {
            "name": "New name",
            "inn": "1234567890",
        }
        url = reverse(
            "signatures:certification-center-detail",
            kwargs={"slug": certification_center.slug},
        )
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCertificateCRUD:
    certificate_list_url = reverse("signatures:certificate-list")

    def test_create_certificate_without_auth(self, api_client):
        data = {
            "file": "New Certificate",
            "position": "1234567890",
            "certification_center": "1234567890",
            "start_date": "2025-07-01",
            "end_date": "2026-07-31",
        }
        response = api_client.post(self.certificate_list_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_certificates(self, api_client):
        CertificateFactory.create_batch(5)
        response = api_client.get(self.certificate_list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_certificate_without_auth(self, api_client):
        certificate = CertificateFactory()
        url = reverse(
            "signatures:certificate-detail", kwargs={"slug": certificate.slug}
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_certificate_without_auth(self, api_client):
        certificate = CertificateFactory()
        data = {
            "file": "New Certificate",
            "position": "1234567890",
            "certification_center": "1234567890",
            "start_date": "2025-07-01",
            "end_date": "2026-07-31",
        }
        url = reverse(
            "signatures:certificate-detail", kwargs={"slug": certificate.slug}
        )
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestElectronicDigitalSignatureCRUD:
    electronic_digital_signature_list_url = reverse(
        "signatures:electronic-digital-signature-list"
    )

    def test_create_electronic_digital_signature_without_auth(self, api_client):
        data = {
            "certificate": "New Electronic Digital Signature",
            "archive": "1234567890",
            "owner": "1234567890",
            "start_date": "2025-07-01",
            "end_date": "2026-07-31",
        }
        response = api_client.post(self.electronic_digital_signature_list_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_electronic_digital_signatures(self, api_client):
        ElectronicDigitalSignatureFactory.create_batch(5)
        response = api_client.get(self.electronic_digital_signature_list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_electronic_digital_signature_without_auth(self, api_client):
        electronic_digital_signature = ElectronicDigitalSignatureFactory()
        url = reverse(
            "signatures:electronic-digital-signature-detail",
            kwargs={"slug": electronic_digital_signature.slug},
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_electronic_digital_signature_without_auth(self, api_client):
        electronic_digital_signature = ElectronicDigitalSignatureFactory()
        data = {
            "certificate": "New Electronic Digital Signature",
            "archive": "1234567890",
            "owner": "1234567890",
            "start_date": "2025-07-01",
            "end_date": "2026-07-31",
        }
        url = reverse(
            "signatures:electronic-digital-signature-detail",
            kwargs={"slug": electronic_digital_signature.slug},
        )
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        electronic_digital_signature = ElectronicDigitalSignatureFactory()
        url = reverse(
            "signatures:electronic-digital-signature-detail",
            kwargs={"slug": electronic_digital_signature.slug},
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
