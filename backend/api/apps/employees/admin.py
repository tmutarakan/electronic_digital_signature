from django.contrib import admin
from core.admin import BaseSettingAdmin
from .models import Passport, INN, SNILS, Employee


class SettingAdminPassport(BaseSettingAdmin):
    fields = ("title", "date_of_issue", "birthdate", "birthplace", "code")
    ordering = ("series", "number")

    def get_list_display(self, request):
        return self.fields + super().get_list_display(request)

    def title(self, obj):
        return f"{obj.series} {obj.number}"


class SettingAdminINN(BaseSettingAdmin):
    fields = ("value",)

    def get_list_display(self, request):
        return self.fields + super().get_list_display(request)


class SettingAdminSNILS(BaseSettingAdmin):
    fields = ("value",)

    def get_list_display(self, request):
        return self.fields + super().get_list_display(request)


class SettingAdminEmployee(BaseSettingAdmin):
    fields = ("fullname", "gender", "passport", "inn", "snils")
    search_fields = ('surname', "name", "patronymic")
    ordering = ('surname', "name", "patronymic")

    def get_list_display(self, request):
        return self.fields + super().get_list_display(request)

    def fullname(self, obj):
        return f"{obj.surname} {obj.name} {obj.patronymic}"


admin.site.register(Passport, SettingAdminPassport)
admin.site.register(INN, SettingAdminINN)
admin.site.register(SNILS, SettingAdminSNILS)
admin.site.register(Employee, SettingAdminEmployee)
