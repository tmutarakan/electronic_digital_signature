from django.contrib import admin
from .models import Sertificate, ElectronicDigitalSignature, CertificationCenter


class SettingAdminSertificate(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminCertificationCenter(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminElectronicDigitalSignature(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Sertificate, SettingAdminSertificate)
admin.site.register(ElectronicDigitalSignature, SettingAdminElectronicDigitalSignature)
admin.site.register(CertificationCenter, SettingAdminCertificationCenter)
