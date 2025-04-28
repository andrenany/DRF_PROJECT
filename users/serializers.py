from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo de Usuario"""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 
                  'is_verified', 'date_joined', 'receive_promotions']
        read_only_fields = ['id', 'date_joined', 'is_verified']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para el registro de nuevos usuarios"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password', 
                  'user_type', 'receive_promotions']
    
    def validate(self, attrs):
        # Verificar que las contraseñas coincidan
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        
        # Eliminar confirm_password del diccionario de atributos
        attrs.pop('confirm_password')
        return attrs
    
    def create(self, validated_data):
        # Crear un nuevo usuario con los datos validados
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            receive_promotions=validated_data.get('receive_promotions', False)
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    """Serializer para el login de usuarios"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})