"""
Serializers definitions of the Django models defined in ./models.py.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *


class SuggestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Suggestion
        fields = ['suggestion', 'reason', 'coach_name', 'coach']
        read_only_fields = ['coach']


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    suggestions = SuggestionSerializer(
        many=True, source='suggestion_set', read_only=True)
    final_decision = SuggestionSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['url', 'id', 'first_name', 'last_name', 'call_name', 'email', 
                  'phone_number', 'alum', 'language', 'extra_info', 'cv', 'portfolio', 
                  'school_name', 'degree', 'studies', 'skills', 'suggestions', 'final_decision']


class CoachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['url', 'id', 'first_name', 'last_name', 'email', 'is_admin', 'is_active']
        read_only_fields = ['is_admin', 'is_active']


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ['url', 'id', 'name', 'color']


class RequiredSkillsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RequiredSkills
        fields = ['amount', 'skill', 'comment']


class ProjectSuggestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectSuggestion
        fields = ['student', 'coach', 'coach_name', 'skill', 'reason']
        read_only_fields = ['coach']


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    required_skills = RequiredSkillsSerializer(
        many=True, source='requiredskills_set')
    suggested_students = ProjectSuggestionSerializer(
        many=True, source='projectsuggestion_set', read_only=True)

    class Meta:
        model = Project
        fields = ['url', 'id', 'name', 'partner_name', 'extra_info',
                  'required_skills', 'coaches', 'suggested_students']

    # overwrite create method to be able to create RequiredSkills objects
    def create(self, validated_data):
        skills_data = validated_data.pop('requiredskills_set')
        coaches = validated_data.pop('coaches')
        project = Project.objects.create(**validated_data)
        project.coaches.set(coaches)
        for skill_data in skills_data:
            RequiredSkills.objects.create(project=project, **skill_data)
        return project
    

    # overwrite update method to be able to create/update/delete RequiredSkills objects
    def update(self, instance, validated_data):
        
        # first update required skills
        skills_data = validated_data.pop('requiredskills_set')
        # update or create skills from request
        for skill_data in skills_data:
            RequiredSkills.objects.update_or_create(project=instance, **skill_data)
        # delete skills not in request
        skills = [skill_data['skill'] for skill_data in skills_data]
        RequiredSkills.objects.filter(project=instance).exclude(skill__in=skills).delete()
        return super().update(instance, validated_data)


class StudentOnlySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectSuggestion
        fields = ['student']


class UpdateCoachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['is_admin', 'is_active']


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Coach.objects.create_user(
            validated_data['email'], validated_data['password'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])

        return user
