from django.contrib import admin
from core.admin import BaseSettingAdmin
from .models import Organization, Position


class SettingAdminOrganization(BaseSettingAdmin):
    fields = ("name", "ogrn", "inn", "kpp", "registered_address")

    def get_list_display(self, request):
        return self.fields + super().get_list_display(request)


class SettingAdminPosition(BaseSettingAdmin):
    fields = ("name", "organization")

    def get_list_display(self, request):
        return self.fields + super().get_list_display(request)


admin.site.register(Organization, SettingAdminOrganization)
admin.site.register(Position, SettingAdminPosition)
