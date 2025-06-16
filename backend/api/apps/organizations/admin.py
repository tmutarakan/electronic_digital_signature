from django.contrib import admin
from .models import Organization, Position


class SettingAdminOrganization(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminPosition(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Organization, SettingAdminOrganization)
admin.site.register(Position, SettingAdminPosition)
