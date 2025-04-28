from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import User

User = get_user_model()

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_str_representation(self):
        """Test que verifica la representación string del usuario (__str__)"""
        self.assertEqual(str(self.user), self.user_data['email'])

    def test_get_full_name_property(self):
        """Test que verifica la propiedad get_full_name"""
        expected_full_name = f"{self.user_data['first_name']} {self.user_data['last_name']}"
        self.assertEqual(self.user.get_full_name, expected_full_name)

    def test_token_method_exists(self):
        """Test que verifica que el método token existe (aunque sea un pass por ahora)"""
        # Simplemente verificamos que el método existe y se puede llamar
        self.user.token()  # No debería lanzar excepción