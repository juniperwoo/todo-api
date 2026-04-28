from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta: #defines how serializer behaves
        model  = Todo #tells to uuser todo model
        fields = '__all__' #include all fields from model like its id, title...
        read_only_fields = ('id', 'created_at', 'updated_at') #defines fields that cant be modified by user

    def validate_title(self, value): # field level validation that runs when user sends data to api
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()