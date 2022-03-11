from django.contrib.auth.models import User, Group
from rest_framework import serializers

from osoc.osoc.models import Project, ProjectNeedsSkills, Student, Coach, Skill


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['url', 'id', 'first_name', 'last_name', 'call_name', 'email', 'phone_number', 'language',
                  'extra_info', 'cv', 'portfolio', 'school_name', 'degree', 'studies', 'skills']

    

class CoachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['url', 'id', 'first_name', 'last_name', 'email', 'is_admin']

class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ['url', 'name', 'description']

class ProjectNeedsSkillsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectNeedsSkills
        fields = ['amount', 'skill']

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    skills = ProjectNeedsSkillsSerializer(many=True)
    class Meta:
        model = Project
        fields = ['url', 'id', 'name', 'partner_name', 'extra_info', 'skills', 'coaches']
    
    def create(self, validated_data):
        skills = validated_data.pop('skills')
        coaches = validated_data.pop('coaches')
        project = Project.objects.create(**validated_data)
        project.coaches.set(coaches)
        for skill_data in skills:
            skill = skill_data.pop('skill')
            ProjectNeedsSkills.objects.create(project=project, skill=skill)
        return project


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
