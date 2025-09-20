from rest_framework import routers
from django.urls import path
from .views import LoginView, LogoutView, ProtectedView, RucApiView, DniApiView, UserViewSet

router = routers.DefaultRouter()
router.register("", UserViewSet)

urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('ruc/<str:number>', RucApiView.as_view(), name='user-ruc'),
    path('dni/<str:number>', DniApiView.as_view(), name='user-dni')

] + router.urls