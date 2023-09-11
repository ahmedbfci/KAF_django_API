from rest_framework import serializers
from .models import my_user
class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_user
        fields = ["user", "name", "salary", "percentage"]