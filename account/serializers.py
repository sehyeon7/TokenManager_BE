from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError
# from .models import UserProfile

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "password", "username"]

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        if not (username and password):
            raise ValidationError({"detail": "[username, password] fields missing."})
        return attrs
    


