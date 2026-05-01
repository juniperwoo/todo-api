from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model  = Todo
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
        
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()