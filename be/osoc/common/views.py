"""
Views that create a connection between the database and the application.
"""
from rest_framework import viewsets, mixins, permissions, status, generics, filters
from rest_framework.response import Response
from rest_framework.views import PermissionDenied
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from django.db.models import RestrictedError
from .filters import *
from .serializers import *
from .models import *
from .pagination import StandardPagination
from .tally.tally import TallyForm
from .permissions import IsAdmin, IsOwnerOrAdmin, IsActive
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed, edited or searched.
    Search students with the query parameter ?search=
    Filter students with the query parameters:
        ?alum=[true, false]
        ?language=string
        ?skills=:id:
        ?student_coach=[true, false]
        ?english_rating=[1-5]
        ?status=[0-5]
        ?on_project=[true, false]
        ?suggested_by_user=[true, false]
        ?suggestion=[yes, no, maybe, none, 0, 1, 2, 3]
    example query: /api/students/?alum=true&status=0&skills=1&suggestion=yes&on_project=true&language=Dutch
    """
    queryset = Student.objects.all().order_by('id')
    pagination_class = StandardPagination
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsActive]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, StudentOnProjectFilter,
                       StudentSuggestedByUserFilter, StudentFinalDecisionFilter]
    search_fields = ['first_name', 'last_name', 'call_name', 'email', 'degree',
                     'studies', 'motivation', 'school_name', 'employment_agreement', 'hinder_work']
    filterset_fields = ['alum', 'language', 'skills',
                        'student_coach', 'english_rating', 'status']

    @action(detail=True, methods=['post'], serializer_class=SuggestionSerializer)
    def make_suggestion(self, request, pk=None):
        """
        let a coach make a suggestion for the current student
        if the coach has already made a suggestion for this student, it is updated
        returns HTTP response:
            400 BAD REQUEST: there was required data missing or the data could not be serialized
            201 CREATED:     a new suggestion was created or updated
        """
        serializer = SuggestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # save suggestion
            serializer.save(student=self.get_object(), coach=request.user, final=False)

            # send data to websocket
            socket_data = serializer.data
            socket_data['student_id'] = pk
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "suggestion",
                {
                    'type': 'suggestion',
                    'data': socket_data
                }
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            student=self.get_object(), coach=request.user, final=False).delete()

        # send data to websocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "suggestion",
            {
                'type': 'remove_suggestion',
                'data': {
                    'student_id': pk,
                    'coach_id': request.user.id
                }
            }
        )

        return Response(status=(status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND))

    @action(detail=True, methods=['post'], serializer_class=SuggestionSerializer,
            permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
    def make_final_decision(self, request, pk=None):
        """
        let an admin make a final decision for the current student
        if the admin has already made a final decision for this student, it is updated
        returns HTTP response:
            400 BAD REQUEST: there was required data missing or the data could not be serialized
            201 CREATED:     the final decision was created or updated
        """
        serializer = SuggestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            student = self.get_object()
            # save suggestion
            suggestion = serializer.save(student=student, coach=request.user, final=True)
            # set final_decision in student
            student.final_decision = suggestion
            student.save()
            
            # send data to websocket
            socket_data = serializer.data
            socket_data['student_id'] = pk
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "suggestion",
                {
                    'type': 'suggestion',
                    'data': socket_data
                }
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], serializer_class=SuggestionSerializer,
            permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
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
            student=self.get_object(), coach=request.user, final=True).delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "suggestion",
            {
                'type': 'final_decision',
                'data': {
                    'student_id': pk
                }
            }
        )

        return Response(status=(status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND))

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def tallyregistration(self, request, pk=None):
        """
        Endpoint to which Tally's webhook can connect to register students.
        returns HTTP response:
            400 BAD REQUEST:  The request data was malformatted or a student tried to register twice
            201 CREATED:    The student registration resulted in a new student being created
        """
        tally = TallyForm.fromFile()
        try:
            form = tally.transform(tally.validate(request.data))
            skillNames = form.pop("skills")
            student = Student.objects.create(**form)
            skills = []
            for skillName in skillNames:
                existingSkill = Skill.objects.filter(name=skillName).first()
                if existingSkill == None:
                    skills.append(Skill.objects.create(name=skillName, color="grey"))
                else:
                    skills.append(existingSkill)
            student.skills.set(skills)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class CoachViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):   # no create, this is handled in RegisterView
    """
    API endpoint that allows coaches to be viewed, edited or searched.
    a coach cannot be created by this API endpoint
    a coach can only update and view its own data, except for admins
    Search coaches with the query parameter ?search=
    Filter coaches with the query parameters
        ?is_admin=[true, false],
        ?is_active=[true, false
    example query: /api/coaches/?is_admin=false&is_active=true
    """
    queryset = Coach.objects.all().order_by('id')
    pagination_class = StandardPagination
    serializer_class = CoachSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsOwnerOrAdmin, IsActive]
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

    @action(detail=True, methods=['put'], serializer_class=UpdateCoachSerializer,
            permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
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
                coach.is_admin = serializer.data.get('is_admin', coach.is_admin)
                coach.is_active = serializer.data.get('is_active', coach.is_active)
                coach.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "you can not update your own admin status"}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed, edited or searched.
    only admin users have permission for this endpoint, except for suggesting students or removing suggestions
    Search projects with the query parameter ?search=
    Filter projects with the query parameters
        ?required_skills=:id:,
        ?coaches=:id:,
        ?suggested_students=:id:
    example query: /api/projects/?required_skills=1&coaches=2&suggested_students=1
    """
    queryset = Project.objects.all().order_by('id')
    pagination_class = StandardPagination
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin, IsActive]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'partner_name', 'extra_info']
    filterset_fields = ['required_skills', 'coaches', 'suggested_students']

    def get_serializer_class(self):
        """
        override method to change serializer class in list and retrieve (GET) requests
        this way more coach information can be returned in project responses,
        but not needed when making POST, PUT, PATCH requests
        """
        if hasattr(self, 'action') and self.action == 'list' or self.action == 'retrieve':
            return ProjectListSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post'], serializer_class=ProjectSuggestionSerializer,
            permission_classes=[permissions.IsAuthenticated, IsActive])
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
        serializer = ProjectSuggestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            project = self.get_object()

            # check if skill is one of the required skills of the project
            skill = serializer.validated_data.get('skill')
            if skill in project.required_skills.all():
                # save projectsuggestion
                serializer.save(project=project, coach=request.user)

                # send data to websocket
                socket_data = serializer.data
                socket_data['project_id'] = pk
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "suggestion",
                    {
                        'type': 'suggest_student',
                        'data': socket_data
                    }
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"detail": "skill must be one of the required skills of the project"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # method should be delete but this is not possible because delete requests cannot handle request body
    @action(detail=True, methods=['post'], serializer_class=RemoveProjectSuggestionSerializer,
            permission_classes=[permissions.IsAuthenticated, IsActive])
    def remove_student(self, request, pk=None):
        """
        let a coach remove a projectsuggestion for this project
        a coach can only remove a projectsuggestion from themselves
        returns HTTP response:
            400 BAD REQUEST: there was required data missing or the data could not be serialized
            404 NOT FOUND:   there was no projectsuggestion found
            204 NO CONTENT:  the projectsuggestion was found and removed
        """
        serializer = RemoveProjectSuggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():

            # delete ProjectSuggestion object if it is found
            deleted, _ = ProjectSuggestion.objects.filter(
                project=self.get_object(),
                **serializer.validated_data
            ).delete()

            # send data to websocket
            socket_data = serializer.data
            socket_data['project_id'] = pk
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "suggestion",
                {
                    'type': 'remove_student',
                    'data': socket_data
                }
            )

            return Response(status=(status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsActive])
    def get_conflicting_projects(self, request):
        """
        get a list of conflicting projects;
        two projects are conflicting if one student has been suggested/assigned to both of them
        """
        students = Student.objects.all()
        conflicts = {}
        for student in students:
            projects = ProjectSuggestion.objects.filter(student=student)
            if projects.count() > 1:
                student_url = request.build_absolute_uri(
                    reverse("student-detail", args=(student.id,)))
                project_urls = [request.build_absolute_uri(reverse("project-detail", args=(project_sug.project.id,)))
                                for project_sug in projects]
                conflicts[student_url] = set(project_urls)
        return Response({"conflicts": conflicts}, status=status.HTTP_200_OK)


class SkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows skills to be viewed, edited or searched.
    Search skills with the query parameter ?search=
    """
    queryset = Skill.objects.all().order_by('id')
    pagination_class = StandardPagination
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated, IsActive]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def destroy(self, request, pk=None):
        if request.user.is_admin:
            try:
                self.perform_destroy(self.get_object())
            except RestrictedError:
                return Response({"detail": "can't delete skill, it is used in at least one project suggestion"},
                                status=status.HTTP_403_FORBIDDEN)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied()


class SentEmailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sent emails to be viewed, edited or searched.
    Search emails with the query parameter ?search=
    Filter emails with the query parameters
        ?sender=:id:,
        ?receiver=:id:,
        ?date=yyyy-mm-dd,
        ?before=yyyy-mm-ddThh:mm:ss,
        ?after=yyyy-mm-ddThh:mm:ss
    example query: /api/emails/?sender=1&after=2022-04-03
    """
    queryset = SentEmail.objects.all().order_by('id')
    serializer_class = SentEmailSerializer
    permission_classes = [permissions.IsAuthenticated, IsActive]
    filter_backends = [filters.SearchFilter,
                       DjangoFilterBackend, EmailDateTimeFilter]
    search_fields = ['info']
    filterset_fields = ['sender', 'receiver']

    def create(self, request):
        serializer = SentEmailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://0.0.0.0:8000/accounts/github/login/callback/"
    client_class = OAuth2Client
