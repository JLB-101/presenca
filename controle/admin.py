from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Turma, Estudante, Docente, Presenca

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'docente', 'ano', 'cadeira', 'total_estudantes', 'evento_presenca')
    search_fields = ('nome', 'docente__user__username')
    list_filter = ('docente', 'ano')

class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo_estudante', 'turma')
    search_fields = ('nome', 'codigo_estudante', 'turma__nome')
    list_filter = ('turma',)

class DocenteAdmin(admin.ModelAdmin):
    list_display = ('user', 'disciplina')
    search_fields = ('user__username', 'disciplina')

class PresencaAdmin(admin.ModelAdmin):
    list_display = ('estudante', 'data', 'presente')
    search_fields = ('estudante__nome',)
    list_filter = ('estudante__turma', 'presente')

admin.site.register(User, UserAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Estudante, EstudanteAdmin)
admin.site.register(Docente, DocenteAdmin)
admin.site.register(Presenca, PresencaAdmin)
