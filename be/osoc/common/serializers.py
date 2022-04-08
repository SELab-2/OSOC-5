"""
Serializers definitions of the Django models defined in ./models.py.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer


class SuggestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Suggestion
        fields = ['suggestion', 'reason', 'coach_name', 'coach_id', 'coach']
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
        fields = ['student', 'coach', 'coach_name', 'coach_id', 'skill', 'reason']
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


class SentEmailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SentEmail
        fields = ['url', 'id', 'sender', 'receiver', 'time', 'info']


class StudentOnlySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectSuggestion
        fields = ['student']


class UpdateCoachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['is_admin', 'is_active']


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.CharField(
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
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
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


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = None

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        }
