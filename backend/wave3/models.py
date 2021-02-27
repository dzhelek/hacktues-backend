from django.db import models

from wave2 import models as wave2models

class Mentor(models.Model):
    technologies = models.ManyToManyField(wave2models.Technology, blank=True)
    profile_picture = models.URLField()
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    was_mentor = models.BooleanField()
    elsys = models.SmallIntegerField(blank=True, null=True)
    organization = models.CharField(max_length=100)
    pozition = models.CharField(max_length=100)
    free = models.TextField()
    tshirt_size = models.CharField(max_length=5)
    agreed = models.TextField()
    xp = models.TextField()
