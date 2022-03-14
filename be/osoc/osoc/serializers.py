from django.contrib.auth.models import User, Group
from rest_framework import serializers

from osoc.osoc.models import Project, RequiredSkills, Student, Coach, Skill, Suggestion, ProjectSuggestion


class SuggestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Suggestion
        fields = ['suggestion', 'reason', 'coach']

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    suggestions = SuggestionSerializer(many=True, source='suggestion_set', required=False)
    class Meta:
        model = Student
        fields = ['url', 'id', 'first_name', 'last_name', 'call_name', 'email', 'phone_number', 'language',
                  'extra_info', 'cv', 'portfolio', 'school_name', 'degree', 'studies', 'skills', 'suggestions']

class CoachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['url', 'id', 'first_name', 'last_name', 'email', 'is_admin']

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
    required_skills = RequiredSkillsSerializer(many=True, source='requiredskills_set')
    suggested_students = ProjectSuggestionSerializer(many=True, source='projectsuggestion_set', required=False)
    class Meta:
        model = Project
        fields = ['url', 'id', 'name', 'partner_name', 'extra_info', 'required_skills', 'coaches', 'suggested_students']
    
    def create(self, validated_data):
        validated_data.pop('projectsuggestion_set') # ignore this field
        skills_data = validated_data.pop('requiredskills_set')
        coaches = validated_data.pop('coaches')
        project = Project.objects.create(**validated_data)
        project.coaches.set(coaches)
        for skill_data in skills_data:
            RequiredSkills.objects.create(project=project, **skill_data)
        return project


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
