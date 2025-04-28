from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    # Tipos de usuario
    class UserType(models.TextChoices):
        ADMINISTRADOR = 'ADMINISTRADOR', _('Administrador')
        VENDEDOR = 'VENDEDOR', _('Vendedor')
        BODEGUERO = 'BODEGUERO', _('Bodeguero')
        CONTADOR = 'CONTADOR', _('Contador')
        CLIENTE = 'CLIENTE', _('Cliente')
    
    # Campos base
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    
    # Tipo de usuario
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CLIENTE,
        verbose_name=_("User Type")
    )
    
    # Campos de control
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Fechas de registro y último acceso
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    # Para recibir promociones (solo para clientes)
    receive_promotions = models.BooleanField(default=False)
    
    # Configuraciones de autenticación
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def token(self):
        # Implementar generación de token para autenticación
        pass
    
    # Personalizar las relaciones con `groups` y `user_permissions`
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Aquí agregamos un nombre único
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Aquí agregamos un nombre único
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )
