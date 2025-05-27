from django.contrib import admin
from .models import (
    Organization,
    Position,
    Passport,
    INN,
    SNILS,
    Employee,
    Sertificate,
    ElectronicDigitalSignature,
)


class SettingAdminOrganization(admin.ModelAdmin):
    def get_list_display(self, request):
        return [
            field.name for field in self.model._meta.fields  # pylint: disable=W0212
        ]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminPosition(admin.ModelAdmin):
    def get_list_display(self, request):
        return [
            field.name for field in self.model._meta.fields  # pylint: disable=W0212
        ]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminPassport(admin.ModelAdmin):
    def get_list_display(self, request):
        return [
            field.name for field in self.model._meta.fields  # pylint: disable=W0212
        ]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminINN(admin.ModelAdmin):
    def get_list_display(self, request):
        return [
            field.name for field in self.model._meta.fields  # pylint: disable=W0212
        ]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminSNILS(admin.ModelAdmin):
    def get_list_display(self, request):
        return [
            field.name for field in self.model._meta.fields  # pylint: disable=W0212
        ]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminEmployee(admin.ModelAdmin):
    def get_list_display(self, request):
        return [
            field.name for field in self.model._meta.fields  # pylint: disable=W0212
        ]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminSertificate(admin.ModelAdmin):
    def get_list_display(self, request):
        return [
            field.name for field in self.model._meta.fields  # pylint: disable=W0212
        ]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminElectronicDigitalSignature(admin.ModelAdmin):
    def get_list_display(self, request):
        return [
            field.name for field in self.model._meta.fields  # pylint: disable=W0212
        ]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Organization, SettingAdminOrganization)
admin.site.register(Position, SettingAdminPosition)
admin.site.register(Passport, SettingAdminPassport)
admin.site.register(INN, SettingAdminINN)
admin.site.register(SNILS, SettingAdminSNILS)
admin.site.register(Employee, SettingAdminEmployee)
admin.site.register(Sertificate, SettingAdminSertificate)
admin.site.register(ElectronicDigitalSignature, SettingAdminElectronicDigitalSignature)
