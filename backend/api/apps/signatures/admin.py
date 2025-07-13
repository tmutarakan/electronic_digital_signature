from django.contrib import admin
from core.admin import BaseSettingAdmin
from .models import Certificate, ElectronicDigitalSignature, CertificationCenter


class SettingAdminCertificate(BaseSettingAdmin):
    fields = ("filename", "file", "position", "certification_center", "start_date", "end_date")

    def get_list_display(self, request):
        return self.fields + super().get_list_display(request)



class SettingAdminCertificationCenter(BaseSettingAdmin):
    fields = ("name", "inn")

    def get_list_display(self, request):
        return self.fields + super().get_list_display(request)



class SettingAdminElectronicDigitalSignature(BaseSettingAdmin):
    fields = ("filename", "sertificate", "archive", "owner", "start_date", "end_date")

    def get_list_display(self, request):
        return self.fields + super().get_list_display(request)



admin.site.register(Certificate, SettingAdminCertificate)
admin.site.register(ElectronicDigitalSignature, SettingAdminElectronicDigitalSignature)
admin.site.register(CertificationCenter, SettingAdminCertificationCenter)
