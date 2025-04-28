from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Manager personalizado para nuestro modelo de Usuario"""
    
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """Crear y guardar un usuario con el email y password dados"""
        if not email:
            raise ValueError(_('El email es obligatorio'))
        
        # Normalizar el email (lowercase en el dominio)
        email = self.normalize_email(email)
        
        # Crear instancia de usuario
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        
        # Establecer y hashear password
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """Crear y guardar un superusuario con el email y password dados"""
        # Asegurar que tenga los permisos apropiados
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, first_name, last_name, password, **extra_fields)