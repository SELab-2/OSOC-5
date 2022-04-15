"""
Views that create a connection between the database and the application.
"""
from rest_framework import viewsets, mixins, permissions, status, generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from django.urls import resolve
from urllib.parse import urlparse
from rest_framework.reverse import reverse
from .models import *
from .permissions import IsAdmin, IsOwnerOrAdmin, IsActive
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed, edited or searched.
    Search students with the query parameter '?search='
    Filter students with the query parameters '?alum=', '?language=', '?skills=', '?on_project', '?suggested_by_user' and '?suggestion='
    example query: /api/students/?alum=true&language=0&skills=1&suggestion=yes&on_project
    """
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsActive]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, StudentOnProjectFilter, StudentSuggestedByUserFilter, StudentFinalDecisionFilter]
    search_fields = ['first_name', 'last_name', 'call_name', 'email', 'alum', 'language', 'degree', 'studies', 'extra_info']
    filterset_fields = ['alum', 'language', 'skills'] # TODO practical info, student coach

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

            response_data = serializer.data
            response_data['coach_name'] = request.user.get_full_name()
            response_data['coach_id'] = request.user.id
            response_data['coach'] = request.build_absolute_uri(reverse("coach-detail", args=(request.user.id,)))
            
            return Response(response_data, status=(status.HTTP_201_CREATED if created else status.HTTP_200_OK))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], serializer_class=SuggestionSerializer)
    def remove_suggestion(self, request, pk=None):
        """
        let a coach remove a suggestion he has made for the current student
        a coach can only remove a suggestion from themselves
        returns HTTP response:
            404 NOT FOUND:      there was no suggestion found
            204 NO CONTENT:     the suggestion was found and removed
        """
        # delete Suggestion object if it is found
        deleted, _ = Suggestion.objects.filter(
            student=self.get_object(), coach=request.user).delete()

        return Response(status=(status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND))
    
    @action(detail=True, methods=['post'], serializer_class=SuggestionSerializer, permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
    def make_final_decision(self, request, pk=None):
        """
        let an admin make a final decision for the current student
        if the admin has already made a final decision for this student, it is updated
        returns HTTP response:
            400 BAD REQUEST: there was required data missing or the data could not be serialized
            201 CREATED:     the final decision was created
            200 OK:          an existing final decision was found for this student from the current user, it was updated
        """
        serializer = SuggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():

            # create Suggestion object if it doesnt exist yet, else update it
            suggestion, created = Suggestion.objects.update_or_create(
                student=self.get_object(), coach=request.user, defaults=serializer.data)
            
            student = self.get_object()
            student.final_decision = suggestion
            student.save()

            response_data = serializer.data
            response_data['coach_name'] = request.user.get_full_name()
            response_data['coach_id'] = request.user.id
            response_data['coach'] = request.build_absolute_uri(reverse("coach-detail", args=(request.user.id,)))
            
            return Response(response_data, status=(status.HTTP_201_CREATED if created else status.HTTP_200_OK))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], serializer_class=SuggestionSerializer, permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
    def remove_final_decision(self, request, pk=None):
        """
        let an admin remove the final decision he has made for the current student
        an admin can only remove a final decision from themselves
        returns HTTP response:
            404 NOT FOUND:      there was no final decision found
            204 NO CONTENT:     the final decision was found and removed
        """
        # delete Suggestion object if it is found
        deleted, _ = Suggestion.objects.filter(
            student=self.get_object(), coach=request.user).delete()

        return Response(status=(status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND))


class CoachViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):   # no create, this is handled in RegisterView
    """
    API endpoint that allows coaches to be viewed, edited or searched.
    a coach cannot be created by this API endpoint
    a coach can only update and view its own data, except for admins
    Search coaches with the query parameter '?search='
    Filter coaches with the query parameters '?is_admin=' and '?is_active='
    example query: /api/coaches/?is_admin=false&is_active=true
    """
    queryset = Coach.objects.all().order_by('id')
    serializer_class = CoachSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin, IsActive]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'email']
    filterset_fields = ['is_admin', 'is_active']

    def destroy(self, request, pk=None):
        # override delete method to add a check
        coach = self.get_object()
        if coach != request.user:
            # check if number of admins would not be zero after the delete
            if not coach.is_admin or Coach.objects.filter(is_admin=True).count() > 1: 
                self.perform_destroy(coach)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "you cannot remove the only admin"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "you cannot remove your own account"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['put'], serializer_class=UpdateCoachSerializer, permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
    def update_status(self, request, pk=None):
        """
        let an admin update admin rights of another user
        returns HTTP response:
            400 BAD REQUEST:    there was required data missing or the data could not be serialized
            403 FORBIDDEN:      the user does not have the rights to do this action, or th user tries to update their own rights
            204 NO CONTENT:     the user was updated
        """
        serializer = UpdateCoachSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():

            coach = self.get_object()
            # check if coach is not current user
            if coach != request.user:
                coach.is_admin = serializer.data['is_admin']
                coach.is_active = serializer.data['is_active']
                coach.save()
            
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "you can not update your own admin status"}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed, edited or searched.
    only admin users have permission for this endpoint, except for suggesting students or removing suggestions 
    Search projects with the query parameter '?search='
    Filter projects with the query parameters '?required_skills=', '?coaches=' and '?suggested_students='
    example query: /api/projects/?required_skills=1&coaches=2&suggested_students=1
    """
    queryset = Project.objects.all().order_by('id')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin, IsActive]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'partner_name', 'extra_info']
    filterset_fields = ['required_skills', 'coaches', 'suggested_students']

    @action(detail=True, methods=['post'], serializer_class=ProjectSuggestionSerializer, permission_classes=[permissions.IsAuthenticated, IsActive])
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

            project = self.get_object()

            # get student object from url
            student_url = data.pop('student')
            student = Student.objects.get(**resolve(urlparse(student_url).path).kwargs)

            # get skill object from url
            skill_url = data.pop('skill')
            skill = Skill.objects.get(**resolve(urlparse(skill_url).path).kwargs)

            # check if skill is one of the required skills of the project
            if skill in project.required_skills.all():
                
                # replace skill url with skill object
                data['skill'] = skill

                # create ProjectSuggestion if it doesnt exist yet, else update it
                _, created = ProjectSuggestion.objects.update_or_create(
                    project=project, student=student, coach=request.user, defaults=data)

                response_data = serializer.data
                response_data['coach'] = request.build_absolute_uri(reverse("coach-detail", args=(request.user.id,)))
                response_data['coach_name'] = request.user.get_full_name()
                response_data['coach_id'] = request.user.id

                return Response(response_data, status=(status.HTTP_201_CREATED if created else status.HTTP_200_OK))
            return Response({"detail": "skill must be one of the required skills of the project"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # method should be delete but this is not possible because delete requests cannot handle request body
    @action(detail=True, methods=['post'], serializer_class=StudentOnlySerializer, permission_classes=[permissions.IsAuthenticated, IsActive])
    def remove_student(self, request, pk=None):
        """
        let a coach remove a projectsuggestion for this project
        a coach can only remove a projectsuggestion from themselves
        returns HTTP response:
            400 BAD REQUEST: there was required data missing or the data could not be serialized
            404 NOT FOUND:   there was no projectsuggestion found
            204 NO CONTENT:  the projectsuggestion was found and removed
        """
        serializer = StudentOnlySerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():

            # get student object from url
            student_url = serializer.data.pop('student')
            student = Student.objects.get(
                **resolve(urlparse(student_url).path).kwargs)

            # delete ProjectSuggestion object if it is found
            deleted, _ = ProjectSuggestion.objects.filter(
                project=self.get_object(), coach=request.user, student=student).delete()

            return Response(status=(status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsActive])
    def get_conflicting_projects(self, request):
        students = Student.objects.all()
        conflicts = []
        for student in students:
            projects = ProjectSuggestion.objects.filter(student=student)
            if projects.count() > 1:
                student_url = request.build_absolute_uri(reverse("student-detail", args=(student.id,)))
                project_urls = [request.build_absolute_uri(reverse("project-detail", args=(project_sug.project.id,))) 
                                for project_sug in projects]
                conflicts.append({student_url: project_urls})
        return Response({"conflicts": conflicts}, status=status.HTTP_200_OK)


class SkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows skills to be viewed, edited or searched.
    Search skills with the query parameter '?search='
    """
    queryset = Skill.objects.all().order_by('id')
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated, IsActive]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class SentEmailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sent emails to be viewed, edited or searched.
    Search emails with the query parameter '?search='
    Filter emails with the query parameters '?sender=', '?receiver=', '?date=', '?before=' and '?after='
    example query: /api/emails/?sender=1&after=2022-04-03
    """
    queryset = SentEmail.objects.all().order_by('id')
    serializer_class = SentEmailSerializer
    permission_classes = [permissions.IsAuthenticated, IsActive]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, EmailDateTimeFilter]
    search_fields = ['info']
    filterset_fields = ['sender', 'receiver']


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


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://0.0.0.0:8000/accounts/github/login/callback/"
    client_class = OAuth2Client
