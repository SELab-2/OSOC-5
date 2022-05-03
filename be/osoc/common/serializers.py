"""
Serializers definitions of the Django models defined in ./models.py.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from .models import Coach, Suggestion, Student, Project, ProjectSuggestion, SentEmail, Skill, RequiredSkills


class CoachPartialSerializer(serializers.HyperlinkedModelSerializer):
    """
    a serializer to show some fields of the coach model,
    used in other serializers
    """
    class Meta:
        model = Coach
        fields = ['url', 'id', 'first_name', 'last_name']

class SuggestionSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for the Suggestion model
    fields: suggestion, reason, coach
    the coach field is read-only because when a suggestion is created/updated, the current user is used
    """
    coach = CoachPartialSerializer(read_only=True)
    class Meta:
        model = Suggestion
        fields = ['suggestion', 'reason', 'coach']

    def create(self, validated_data):
        """
        override create method to make it update_or_create;
        when a suggestion is found with the same student, coach and final state, it is updated,
        otherwise it is created
        """
        student = validated_data.pop('student')
        coach = validated_data.pop('coach')
        final = validated_data.pop('final')
        # create Suggestion if it doesnt exist yet, else update it
        suggestion, _ = Suggestion.objects.update_or_create(
            student=student, coach=coach, final=final, defaults=validated_data)
        return suggestion


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for the student model
    fields: all student fields
    suggestions and final_decision are read-only
    """
    suggestions = SuggestionSerializer(
        many=True, source='suggestion_set', read_only=True)
    final_decision = SuggestionSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
        extra_fields = ['id']

    def get_field_names(self, declared_fields, info):
        # Include all fields and id
        # https://stackoverflow.com/questions/38245414/django-rest-framework-how-to-include-all-fields-and-a-related-field-in-mo
        expanded_fields = super().get_field_names(
            declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return self.Meta.extra_fields + expanded_fields
        return expanded_fields


class CoachSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for the coach model
    fields: first_name, last_name, email, is_admin and is_active
    is_admin and is_active are read-only
    """
    class Meta:
        model = Coach
        fields = ['url', 'id', 'first_name', 'last_name',
                  'email', 'is_admin', 'is_active']
        read_only_fields = ['is_admin', 'is_active']


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for the skill model
    fields: name, color
    """
    class Meta:
        model = Skill
        fields = ['url', 'id', 'name', 'color']


class RequiredSkillsSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for the RequiredSkills model
    fields: amount, skill, comment
    no url and id fields because the RequiredSkills model does not need API endpoints
    """
    class Meta:
        model = RequiredSkills
        fields = ['amount', 'skill', 'comment']


class ProjectSuggestionSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for the ProjectSuggestion model
    fields: student, coach, skill and reason
    coach is read-only
    no url and id fields because the ProjectSuggestion model does not need API endpoints
    """
    coach = CoachPartialSerializer(read_only=True)
    class Meta:
        model = ProjectSuggestion
        fields = ['student', 'coach', 'skill', 'reason']
        extra_kwargs = {'student': {'required': True, 'allow_null': False}}

    def create(self, validated_data):
        """
        override create method to make it update_or_create;
        when a projectsuggestion is found with the same project, student, coach and skill, it is updated,
        otherwise it is created
        """
        project = validated_data.pop('project')
        student = validated_data.pop('student')
        coach = validated_data.pop('coach')
        skill = validated_data.pop('skill')
        # create ProjectSuggestion if it doesnt exist yet, else update it
        projectsuggestion, _ = ProjectSuggestion.objects.update_or_create(
            project=project, student=student, coach=coach, skill=skill, defaults=validated_data)
        return projectsuggestion


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for the project model
    fields: name, partner_name, extra_info, required_skills, coaches and suggested_students
    required_skills and suggested_students are read-only
    """
    required_skills = RequiredSkillsSerializer(
        many=True, source='requiredskills_set')
    suggested_students = ProjectSuggestionSerializer(
        many=True, source='projectsuggestion_set', read_only=True)

    class Meta:
        model = Project
        fields = ['url', 'id', 'name', 'partner_name', 'extra_info',
                  'required_skills', 'coaches', 'suggested_students']

    def create(self, validated_data):
        """
        override create method to be able to create RequiredSkills objects,
        this is needed because required_skills is a many-to-many field with a through model
        (because it needs an extra 'amount' field)
        """
        skills_data = validated_data.pop('requiredskills_set')
        coaches = validated_data.pop('coaches')
        project = Project.objects.create(**validated_data)
        project.coaches.set(coaches)
        for skill_data in skills_data:
            RequiredSkills.objects.create(project=project, **skill_data)
        return project

    def update(self, instance, validated_data):
        """
        override create method to be able to create/update/remove RequiredSkills objects,
        this is needed because required_skills is a many-to-many field with a through model
        (because it needs an extra 'amount' field)
        """
        # first update required skills
        skills_data = validated_data.pop('requiredskills_set')
        # update or create skills from request
        for skill_data in skills_data:
            RequiredSkills.objects.update_or_create(
                project=instance, **skill_data)
        # delete skills not in request
        skills = [skill_data['skill'] for skill_data in skills_data]
        RequiredSkills.objects.filter(
            project=instance).exclude(skill__in=skills).delete()
        return super().update(instance, validated_data)


class ProjectGetSerializer(ProjectSerializer):
    """
    serializer class to show coach info in project list and project instance, but not in post, put, etc
    """
    coaches = CoachPartialSerializer(many=True)


class SentEmailSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for the sentemail model
    fields: sender, receiver, time, info
    sender and time are read-only
    sender is the current user
    """
    sender = CoachPartialSerializer(read_only=True)
    class Meta:
        model = SentEmail
        fields = ['url', 'id', 'sender', 'receiver', 'time', 'info']
        read_only_fields = ['time']
        extra_kwargs = {'receiver': {'required': True, 'allow_null': False}}


class RemoveProjectSuggestionSerializer(serializers.HyperlinkedModelSerializer):
    """
    a serializer for the remove_student API endpoint to be able to remove a ProjectSuggestion
    only the fields student, coach and skill are needed here
    """
    class Meta:
        model = ProjectSuggestion
        fields = ['student', 'coach', 'skill']


class UpdateCoachSerializer(serializers.HyperlinkedModelSerializer):
    """
    a serializer for the update_coach_status API endpoint
    only the fields is_admin and is_active are needed here
    """
    class Meta:
        model = Coach
        fields = ['is_admin', 'is_active']


class CustomLoginSerializer(LoginSerializer): # pylint: disable=abstract-method
    """
    serializer for the login API endpoint
    """
    username = None
    email = serializers.CharField(
        label="Email",
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

class CustomRegisterSerializer(RegisterSerializer): # pylint: disable=abstract-method
    """
    serializer for the register API endpoint
    """
    username = None
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_admin = serializers.BooleanField()
    is_active = serializers.BooleanField()
    def get_cleaned_data(self):
        super().get_cleaned_data()
        fields = ['password1', 'password2', 'email', 'first_name', 'last_name', 'is_admin', 'is_active']
        return {field: self.validated_data.get(field, '') for field in fields} # pylint: disable=no-member
