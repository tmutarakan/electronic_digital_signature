from django.contrib import admin


class BaseSettingAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        if request.user.is_superuser:
            return (
                "created_at",
                "updated_at",
                "created_by",
                "modified_by",
                "slug",
            )
        return ()

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
