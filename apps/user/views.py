from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer, ModuleSerializer, UserPermissionSerializer
from .models import User, Module, UserPermission

import requests

class CustomPagination(PageNumberPagination):

    page_size = 5  # Número de registros por página
    page_size_query_param = 'page_size'  # Permite cambiar el tamaño desde la URL
    max_page_size = 100  # Tamaño máximo permitido

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Se requieren username y contraseña."}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                return Response({"error": "Cuenta desactivada."}, status=403)

            # Crear o recuperar token
            token, created = Token.objects.get_or_create(user=user)

            # Obtener permisos del usuario
            permissions = UserPermission.objects.filter(user=user).select_related('module')

            permissions_data = [
                {
                    "module_id": perm.module.id,
                    "module": perm.module.code,
                    "name": perm.module.name,
                }
                for perm in permissions
            ]

            user_data = {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "is_admin": user.is_admin,
                "token": token.key,
                "permissions": permissions_data,
            }

            return Response(user_data, status=200)

        return Response({"error": "Credenciales inválidas."}, status=401)
      
class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
             
            request.user.auth_token.delete()
            return Response({"message": "Logout exitoso."}, status=200)
        
        except:

             return Response({"error": "Error al realizar el logout."}, status=400)

class ProtectedView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({"message": "Accediste a una ruta protegida"}, status=200)
    
class RucApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, number):

        # Construcción del endpoint y encabezados
        url = f"https://apifoxperu.net/api/ruc/{number}"
        token = "LFn46Swn6FyiDG5MwGzjMAeZXxp3MLPi1P9W9njJ"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            # Solicitud al servicio externo
            response = requests.get(url, headers=headers, timeout=10)

            # Validar respuesta
            if response.status_code == 200:
                return Response(response.json())
            else:
                return Response(
                    {"error": f"Error al consultar el servicio externo. details {response.json()}"}, status=response.status_code,
                )
        except requests.RequestException as e:
            # Manejo de excepciones en caso de error de conexión o tiempo de espera
            return Response(
                {"error": f"Error al conectar con el servicio externo. details {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        
class DniApiView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get(self, request, number):

        # Construcción del endpoint y encabezados
        url = f"https://apifoxperu.net/api/dni/{number}"
        token = "LFn46Swn6FyiDG5MwGzjMAeZXxp3MLPi1P9W9njJ"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            # Solicitud al servicio externo
            response = requests.get(url, headers=headers, timeout=10)

            # Validar respuesta
            if response.status_code == 200:
                return Response(response.json())
            else:
                return Response(
                    response.json(), status=response.status_code,
                )
        except requests.RequestException as e:
            # Manejo de excepciones en caso de error de conexión o tiempo de espera
            return Response(
                {"error": f"Error al conectar con el servicio externo. details {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        
class UserViewSet(ModelViewSet):

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        user = self.request.user

        # Si es staff → ve todos los usuarios
        if user.is_staff:
            return User.objects.all().order_by('id')

        # Si es admin → ve todos menos los staff
        elif user.is_admin:
            return User.objects.filter(is_staff=False).order_by('id')

        # Otros usuarios → lista vacía
        else:
            return User.objects.none()

class ModuleViewSet(ModelViewSet):

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class UserPermissionViewSet(ModelViewSet):

    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer

    def get_queryset(self):

        user_id = self.request.query_params.get('user')
        if user_id:
            return UserPermission.objects.filter(user_id=user_id)
        return super().get_queryset()

class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user = request.user

        # Obtener permisos del usuario
        permissions = UserPermission.objects.filter(user=user).select_related('module')

        permissions_data = [
            {
                "module_id": perm.module.id,
                "module": perm.module.code,
                "name": perm.module.name,
            }
            for perm in permissions
        ]

        user_data = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "is_admin": user.is_admin,
            "is_staff": user.is_staff,
            "email": user.email,
            "permissions": permissions_data,
        }

        return Response(user_data, status=200)