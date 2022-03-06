from django.contrib.auth.models import User, Group
from rest_framework import serializers

from osoc.osoc.models import Student, Coach, Student


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['url', 'id', 'first_name', 'surname', 'email', 'phone_number', 'language',
                  'extra_info', 'cv', 'portfolio', 'last_email_sent' ]

class CoachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['url', 'id', 'first_name', 'surname', 'email', 'isAdmin', 'last_email_sent']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
