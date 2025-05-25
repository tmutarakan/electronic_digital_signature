from django.contrib import admin
from .models import (
    Organization,
    Position,
    CivilDocument,
    Employee,
    ElectronicDigitalSignature,
)


class SettingAdminOrganization(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]    # pylint: disable=W0212


class SettingAdminPosition(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]    # pylint: disable=W0212


class SettingAdminCivilDocument(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]    # pylint: disable=W0212


class SettingAdminEmployee(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]    # pylint: disable=W0212

    def save_model(self, request, obj, form, change):
        if not change: # Проверяем что запись только создаётся
            obj.author = request.user
        super().save_model(request, obj, form, change)


class SettingAdminElectronicDigitalSignature(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]    # pylint: disable=W0212


admin.site.register(Organization, SettingAdminOrganization)
admin.site.register(Position, SettingAdminPosition)
admin.site.register(CivilDocument, SettingAdminCivilDocument)
admin.site.register(Employee, SettingAdminEmployee)
admin.site.register(ElectronicDigitalSignature, SettingAdminElectronicDigitalSignature)
