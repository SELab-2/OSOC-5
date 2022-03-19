from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Project, RequiredSkills, Student, Coach, Skill, ProjectSuggestion, Suggestion


class SuggestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Suggestion
        fields = ['suggestion', 'reason', 'coach']


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    suggestions = SuggestionSerializer(
        many=True, source='suggestion_set', required=False)

    class Meta:
        model = Student
        fields = ['url', 'id', 'first_name', 'last_name', 'call_name', 'email', 'phone_number', 'language',
                  'extra_info', 'cv', 'portfolio', 'school_name', 'degree', 'studies', 'skills', 'suggestions']


class CoachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['url', 'id', 'first_name', 'last_name', 'email', 'is_admin']


# class ProjectSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['url', 'id', 'name', 'partner_name',
#                   'extra_info', 'skills', 'coaches']


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ['url', 'name', 'description']


class RequiredSkillsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RequiredSkills
        fields = ['amount', 'skill']


class ProjectSuggestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectSuggestion
        fields = ['student', 'coach', 'role', 'reason']


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    required_skills = RequiredSkillsSerializer(
        many=True, source='requiredskills_set')
    suggested_students = ProjectSuggestionSerializer(
        many=True, source='projectsuggestion_set', required=False)

    class Meta:
        model = Project
        fields = ['url', 'id', 'name', 'partner_name', 'extra_info',
                  'required_skills', 'coaches', 'suggested_students']

    def create(self, validated_data):
        validated_data.pop('projectsuggestion_set')  # ignore this field
        skills_data = validated_data.pop('requiredskills_set')
        coaches = validated_data.pop('coaches')
        project = Project.objects.create(**validated_data)
        project.coaches.set(coaches)
        for skill_data in skills_data:
            RequiredSkills.objects.create(project=project, **skill_data)
        return project


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


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
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Coach.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])

        return user
