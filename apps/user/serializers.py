# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'username', 'surname', 'phone', 'is_active', 'is_staff', 'password']
        # O cualquier otro campo que quieras exponer

    def create(self, validated_data):
        """
        Sobrescribimos create() para manejar el password con set_password.
        """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # Encripta la contraseña
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Si actualizas un usuario y viene un 'password', lo encriptamos.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
