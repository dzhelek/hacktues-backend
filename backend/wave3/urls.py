from django.urls import include, path

from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register('mentors', views.MentorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
