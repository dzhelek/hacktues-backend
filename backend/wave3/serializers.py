from rest_framework import serializers

from wave2.serializers import TechnologyField
from .models import Mentor

class MentorSerializer(serializers.ModelSerializer):
    technologies = TechnologyField(many=True)

    class Meta:
        model = Mentor
        fields = ('id', 'technologies', 'profile_picture', 'full_name',
                  'elsys', 'organization', 'pozition', 'free')
