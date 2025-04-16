from rest_framework import serializers

from .models import Profile

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'logo']
