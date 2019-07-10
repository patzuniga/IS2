# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Perfil
from .models import Interes_Personal

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Usuario
from .models import Valoracion

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ['username','password', 'id',]


#admin.site.unregister(Usuario)
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Perfil)
admin.site.register(Interes_Personal)
admin.site.register(Valoracion)