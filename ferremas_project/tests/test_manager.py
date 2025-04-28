from django.test import TestCase
from django.contrib.auth import get_user_model
from users.managers import UserManager

User = get_user_model()

class UserManagerTests(TestCase):
    def setUp(self):
        self.manager = UserManager()
        self.manager.model = User

    def test_create_user_without_email_raises_error(self):
        """Test que verifica que se levante error cuando no se proporciona email"""
        with self.assertRaises(ValueError) as context:
            self.manager.create_user(
                email='',
                first_name='Test',
                last_name='User',
                password='testpass123'
            )
        self.assertEqual(str(context.exception), 'El email es obligatorio')

    def test_create_superuser_default_values(self):
        """Test que verifica los valores por defecto al crear superusuario"""
        superuser = self.manager.create_superuser(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='adminpass123'
        )
        
        # Verificar que los campos están configurados correctamente
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_verified)
        self.assertTrue(superuser.is_active)

    def test_create_superuser_without_staff_raises_error(self):
        """Test que verifica error cuando is_staff no es True"""
        with self.assertRaises(ValueError) as context:
            self.manager.create_superuser(
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                password='adminpass123',
                is_staff=False
            )
        self.assertEqual(str(context.exception), 'Superuser must have is_staff=True.')

    def test_create_superuser_without_superuser_raises_error(self):
        """Test que verifica error cuando is_superuser no es True"""
        with self.assertRaises(ValueError) as context:
            self.manager.create_superuser(
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                password='adminpass123',
                is_superuser=False
            )
        self.assertEqual(str(context.exception), 'Superuser must have is_superuser=True.')