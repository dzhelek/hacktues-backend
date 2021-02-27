from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Mentor
from .serializers import MentorSerializer

class MentorViewSet(ReadOnlyModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
