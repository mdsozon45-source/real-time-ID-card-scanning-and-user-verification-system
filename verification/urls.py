from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, IDCardViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'idcards', IDCardViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
