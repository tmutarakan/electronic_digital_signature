from django.contrib import admin
from .models import (
    Organization,
    Position,
    CivilDocument,
    Employee,
    ElectronicDigitalSignature,
)


class SettingAdminOrganization(admin.ModelAdmin):
    list_display = ("title", "ogrn", "inn", "kpp", "registered_address")


class SettingAdminPosition(admin.ModelAdmin):
    list_display = ("title", "organization")


class SettingAdminCivilDocument(admin.ModelAdmin):
    list_display = (
        "series",
        "number",
        "date_of_issue",
        "birthdate",
        "birthplace",
        "code",
        "inn",
        "snils",
    )


class SettingAdminEmployee(admin.ModelAdmin):
    list_display = (
        "surname",
        "name",
        "patronymic",
        "gender",
        "position",
        "civil_document",
        "slug",
        "created_at",
    )


class SettingAdminElectronicDigitalSignature(admin.ModelAdmin):
    list_display = ("title", "sertificate", "archive", "owner")


admin.site.register(Organization, SettingAdminOrganization)
admin.site.register(Position, SettingAdminPosition)
admin.site.register(CivilDocument, SettingAdminCivilDocument)
admin.site.register(Employee, SettingAdminEmployee)
admin.site.register(ElectronicDigitalSignature, SettingAdminElectronicDigitalSignature)
