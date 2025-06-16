from django.contrib import admin
from .models import Passport, INN, SNILS, Employee


class SettingAdminPassport(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminINN(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminSNILS(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class SettingAdminEmployee(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Passport, SettingAdminPassport)
admin.site.register(INN, SettingAdminINN)
admin.site.register(SNILS, SettingAdminSNILS)
admin.site.register(Employee, SettingAdminEmployee)
