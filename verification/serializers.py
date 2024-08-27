from rest_framework import serializers
from .models import User, IDCard

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class IDCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDCard
        fields = '__all__'
