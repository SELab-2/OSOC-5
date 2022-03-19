from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from rest_framework import viewsets, mixins, permissions, views, status, generics
from .serializers import SkillSerializer, UserSerializer, GroupSerializer, StudentSerializer, CoachSerializer, ProjectSerializer, RegisterSerializer, SuggestionSerializer, ProjectSuggestionSerializer
from rest_framework.response import Response
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from django.urls import resolve
from urllib.parse import urlparse
from .models import Skill, Student, Coach, Project, Suggestion, ProjectSuggestion


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], serializer_class=SuggestionSerializer)
    def make_suggestion(self, request, pk=None):
        """
        lets a coach make a suggestion for the current student
        if the coach has already made a suggestion for this student, it is updated
        """
        serializer = SuggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.data

            # get coach object from url
            # TODO coach must be current user -> request.user.id, needs session-auth branch
            coach_url = data.pop('coach')
            coach = Coach.objects.get(
                **resolve(urlparse(coach_url).path).kwargs)

            # create Suggestion if it doesnt exist yet, else update it
            _, created = Suggestion.objects.update_or_create(
                student=self.get_object(), coach=coach, defaults=data)
            return Response({"data": serializer.data, "status": "created" if created else "updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoachViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows coaches to be viewed or edited.
    """
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], serializer_class=ProjectSuggestionSerializer)
    def suggest_student(self, request, pk=None):
        serializer = ProjectSuggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.data

            # get coach object from url
            # TODO coach must be current user -> request.user.id, needs session-auth branch
            coach_url = data.pop('coach')
            coach = Coach.objects.get(
                **resolve(urlparse(coach_url).path).kwargs)

            # get student object from url
            student_url = data.pop('student')
            student = Student.objects.get(
                **resolve(urlparse(student_url).path).kwargs)

            # replace skill url with skill object
            skill_url = data.pop('role')
            data['role'] = Skill.objects.get(
                **resolve(urlparse(skill_url).path).kwargs)

            # create ProjectSuggestion if it doesnt exist yet, else update it
            _, created = ProjectSuggestion.objects.update_or_create(
                project=self.get_object(), student=student, coach=coach, defaults=data)
            return Response({"data": serializer.data, "status": "created" if created else "updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], serializer_class=ProjectSuggestionSerializer)
    def remove_student(self, request, pk=None):
        serializer = ProjectSuggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            # get coach object from url
            coach_url = serializer.data.pop('coach')
            coach = Coach.objects.get(
                **resolve(urlparse(coach_url).path).kwargs)

            # get student object from url
            student_url = serializer.data.pop('student')
            student = Student.objects.get(
                **resolve(urlparse(student_url).path).kwargs)

            # delete ProjectSuggestion object if it is found
            deleted, _ = ProjectSuggestion.objects.filter(
                project=self.get_object(), coach=coach, student=student).delete()
            return Response({"data": serializer.data, "status": "deleted" if deleted else "not found"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin):
    """
    API endpoint that allows skills to be listed, created and deleted.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Coach.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    @classmethod
    def get_extra_actions(cls):
        return []

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
                                                 context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    @classmethod
    def get_extra_actions(cls):
        return []

    def get(self, request):
        logout(request)
        return Response()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.IsAdminUser,)

    @classmethod
    def get_extra_actions(cls):
        return []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": CoachSerializer(user, context=self.get_serializer_context()).data
        })
