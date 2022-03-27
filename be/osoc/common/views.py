"""
Views that create a connection between the database and the application.
"""
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from rest_framework import viewsets, mixins, permissions, views, status, generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from django.urls import resolve
from urllib.parse import urlparse
from .models import *
from .permissions import IsAdmin, IsOwnerOrAdmin

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
        let a coach make a suggestion for the current student
        if the coach has already made a suggestion for this student, it is updated
        returns HTTP response:
            400 BAD REQUEST: there was required data missing or the data could not be serialized
            201 CREATED:     a new suggestion was created
            200 OK:          an existing suggestion was found for this student from the current user, the found suggestion was updated
        """
        serializer = SuggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():

            # create Suggestion object if it doesnt exist yet, else update it
            _, created = Suggestion.objects.update_or_create(
                student=self.get_object(), coach=request.user, defaults=serializer.data)
            
            return Response(serializer.data, status=(status.HTTP_201_CREATED if created else status.HTTP_200_OK))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoachViewSet(viewsets.GenericViewSet, 
                   mixins.ListModelMixin, 
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    """
    API endpoint that allows coaches to be viewed or removed.
    a coach cannot be created by this API endpoint
    a coach can only update and view its own data, except for admins
    """
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    @action(detail=True, methods=['put'])
    def make_admin(self, request, pk=None):
        """
        let an admin give admin rights to another user
        """
        coach = self.get_object()
        coach.is_admin = True
        coach.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['put'])
    def remove_admin(self, request, pk=None):
        """
        let an admin remove admin rights from another user
        """
        coach = self.get_object()
        if coach != request.user:
            coach.is_admin = False
            coach.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    only admin users have permission for this endpoint, except for suggesting students or removing suggestions 
    """
    queryset = Project.objects.all().order_by('id')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @action(detail=True, methods=['post'], serializer_class=ProjectSuggestionSerializer)
    def suggest_student(self, request, pk=None):
        """
        let a coach suggest a student for this project
        if the coach has already suggested this student for this project, the suggestion is updated
        returns HTTP response:
            400 BAD REQUEST: there was required data missing or the data could not be serialized
            201 CREATED:     a new projectsuggestion was created
            200 OK:          an existing projectsuggestion was found for this student and project from the current user, 
                             the found projectsuggestion was updated
        """
        serializer = ProjectSuggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.data

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
                project=self.get_object(), student=student, coach=request.user, defaults=data)

            return Response(serializer.data, status=(status.HTTP_201_CREATED if created else status.HTTP_200_OK))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], serializer_class=ProjectSuggestionSerializer)
    def remove_student(self, request, pk=None):
        """
        let a coach remove a projectsuggestion for this project
        a coach can only remove a projectsuggestion from themselves
        returns HTTP response:
            400 BAD REQUEST: there was required data missing or the data could not be serialized
            404 NOT FOUND:   there was no projectsuggestion found
            200 OK:          the projectsuggestion was found and removed
        """
        serializer = ProjectSuggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():

            # get student object from url
            student_url = serializer.data.pop('student')
            student = Student.objects.get(
                **resolve(urlparse(student_url).path).kwargs)

            # delete ProjectSuggestion object if it is found
            deleted, _ = ProjectSuggestion.objects.filter(
                project=self.get_object(), coach=request.user, student=student).delete()

            return Response(serializer.data, status=(status.HTTP_200_OK if deleted else status.HTTP_404_NOT_FOUND))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows skills to be listed, created and deleted.
    """
    queryset = Skill.objects.all().order_by('id')
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginView(views.APIView):
    """
    API view that handles logging in users; Accessible to anyone.
    """
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    @classmethod
    def get_extra_actions(cls):
        return []

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                                 context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(views.APIView):
    """
    API view that handles logging out users; Accessible to anyone.
    """
    permission_classes = (permissions.AllowAny,)

    @classmethod
    def get_extra_actions(cls):
        return []

    def get(self, request):
        logout(request)
        return Response()


class RegisterView(generics.GenericAPIView):
    """
    API view that handles registering users; Only admins can
    register new users.
    """
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
