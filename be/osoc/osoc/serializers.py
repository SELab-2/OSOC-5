from django.contrib.auth.models import User, Group
from rest_framework import serializers

from osoc.osoc.models import Project, Student, Coach, Skill


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
        fields = ['url', 'id', 'name', 'partner_name', 'extra_info', 'skills', 'coaches']

class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ['url', 'name', 'description']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
