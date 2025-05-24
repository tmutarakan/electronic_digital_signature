import os
from django.core.exceptions import ValidationError


def validate_file_sertificate(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.cer']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Неподдерживаемое расширение файла.')


def validate_file_archive(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.zip']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Неподдерживаемое расширение файла.')
