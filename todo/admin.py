from django.contrib import admin
from .models import ToDo


class Todoadmin(admin.ModelAdmin):
    randomly_fields = ('created',)
admin.site.register(ToDo, Todoadmin)
