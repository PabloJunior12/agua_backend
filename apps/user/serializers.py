# serializers.py
from rest_framework import serializers
from .models import User, Module, UserPermission

# from apps.agua.serializers import ModuleSerializer

# class UserPermissionSerializer(serializers.ModelSerializer):
#     module = ModuleSerializer(read_only=True)
#     module_id = serializers.PrimaryKeyRelatedField(
#         queryset=Module.objects.all(), source='module', write_only=True
#     )

#     class Meta:
#         model = UserPermission
#         fields = ['id', 'module', 'module_id', 'can_view', 'can_edit', 'can_delete']


class ModuleSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ["id", "name", "code", "icon", "children","path"]

    def get_children(self, obj):
        return ModuleSerializer(obj.children.all(), many=True).data
    

class UserPermissionSerializer(serializers.ModelSerializer):

    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())

    class Meta:
        model = UserPermission
        fields = ['module']

class UserSerializer(serializers.ModelSerializer):
    permissions = UserPermissionSerializer(many=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'username', 'surname', 'phone',
            'is_active', 'is_staff', 'is_admin', 'password', 'permissions'
        ]

    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions', [])
        password = validated_data.pop('password', None)

        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        # Crear permisos asociados
        for perm in permissions_data:
            UserPermission.objects.create(user=user, module=perm['module'])

        return user

    def update(self, instance, validated_data):
        permissions_data = validated_data.pop('permissions', None)
        password = validated_data.pop('password', None)

        # Actualizar campos básicos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        # Actualizar permisos si vienen en el request
        if permissions_data is not None:
            instance.permissions.all().delete()  # limpiar permisos actuales
            for perm in permissions_data:
                UserPermission.objects.create(user=instance, module=perm['module'])

        return instance

