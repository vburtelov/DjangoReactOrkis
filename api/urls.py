from django.urls import path
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('client', ClientViewSet, basename="client")
router.register('passport', PassportViewSet, basename="passport")

urlpatterns = []
urlpatterns += router.urls
