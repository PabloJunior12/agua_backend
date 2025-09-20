from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer
from .models import User

import requests

class CustomPagination(PageNumberPagination):

    page_size = 5  # Número de registros por página
    page_size_query_param = 'page_size'  # Permite cambiar el tamaño desde la URL
    max_page_size = 100  # Tamaño máximo permitido

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')  # Ahora esperas 'username'
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Se requieren username y contraseña."}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=200)
            else:
                return Response({"error": "Cuenta desactivada."}, status=403)
        else:
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
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination