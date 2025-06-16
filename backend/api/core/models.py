from django.db import models
from django.contrib.auth.models import User


from .utils import unique_slugify


class TrackChanges(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Автор",
        related_name="%(app_label)s_%(class)s_created_by",
    )
    modified_by = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        editable=False,
        verbose_name="Изменено",
        related_name="%(app_label)s_%(class)s_modified_by",
    )
    slug = models.SlugField(verbose_name="ЧПУ", editable=False, unique=True)

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, str(self))
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
