from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import authenticate

from osoc.common.models import Project, Student, Coach, Skill


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['url', 'id', 'first_name', 'last_name', 'call_name', 'email', 'phone_number', 'language',
                  'extra_info', 'cv', 'portfolio', 'school_name', 'degree', 'studies', 'skills']


class CoachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['url', 'id', 'first_name', 'last_name', 'email', 'is_admin']


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['url', 'id', 'name', 'partner_name',
                  'extra_info', 'skills', 'coaches']


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ['url', 'name', 'description']


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
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
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
