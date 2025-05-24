from django.contrib import admin
from .models import Organization, Position, CivilDocument, Employee, ElectronicDigitalSignature

admin.site.register(Organization)
admin.site.register(Position)
admin.site.register(CivilDocument)
admin.site.register(Employee)
admin.site.register(ElectronicDigitalSignature)
