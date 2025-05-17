from rest_framework import serializers
from .models import User, City, Skill

class CitySerializer(serializers.ModelSerializer):
    """Serializer for the City model"""

    class Meta:
        model = City
        fields = ['id', 'name']

class SkillSerializer(serializers.ModelSerializer):
    """Serializer for the Skill model"""

    class Meta:
        model = Skill
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""
    # Nested representation of city
    city = CitySerializer(read_only=True)
    # Get city by id for write operations
    city_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=City.objects.all(),
        source='city',
        required=False
    )

    # Nested representation of skills
    skills = SkillSerializer(many=True, read_only=True)
    # Get skills by ids for write operations
    skill_ids = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Skill.objects.all(),
        source='skills',
        many=True,
        required=False
    )

    # Get the email from the auth_user
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'auth_user', 'skills', 'skill_ids', 'city', 'city_id']

    def get_email(self, obj):
        return obj.auth_user.email if obj.auth_user else None