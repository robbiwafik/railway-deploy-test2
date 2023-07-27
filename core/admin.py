from typing import Any, Dict, List, Optional, Tuple
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http.request import HttpRequest
from django.db.models import Q

from . import models

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'first_name', 'last_name']
    search_fields = ['username']
    add_fieldsets = [
            (
                None, {
                    "classes": ("wide",),
                    "fields": ("first_name", "last_name", "email", 
                            "is_staff", "username", "password1", 
                            "password2"),
                },
            ),
            ('Permissions', {'fields': ('groups', )})
        ]
    fieldsets = [
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (None, {"fields": ("is_staff", "username", "password")}),
        ('Permissions', {'fields': ('groups', )})
    ]

    def get_queryset(self, request):
        if hasattr(request.user, 'upttik'):
            return models.User.objects.filter(
                upttik__isnull=True,
                staffprodi__isnull=False,
                mahasiswa__isnull=True,
            )
        elif hasattr(request.user, 'staffprodi'):
            prodi = request.user.staffprodi.prodi
            return models.User.objects.filter(
                Q(dosen__isnull=False, dosen__prodi=prodi) |
                Q(mahasiswa__isnull=False, mahasiswa__kelas__prodi=prodi) &
                Q(upttik__isnull=True, staffprodi__isnull=True)
            )
        return super().get_queryset(request)
    
