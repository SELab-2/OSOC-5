"""
Views that create a connection between the database and the application.
"""
# pylint: disable=invalid-name
from rest_framework import viewsets, mixins, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import PermissionDenied
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import RegisterView, SocialLoginView
from django.db.models import RestrictedError, Prefetch
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .utils import export_to_csv, create_zipfile_response
from .pagination import StandardPagination
from .filters import StudentOnProjectFilter, StudentSuggestedByUserFilter, \
    StudentFinalDecisionFilter, EmailDateTimeFilter
from .serializers import BulkStatusSerializer, CSVCoachSerializer, CSVProjectSerializer, CSVProjectSuggestionSerializer, CSVRequiredSkillSerializer, CSVSentEmailSerializer, CSVSkillSerializer, CSVStudentSerializer, CSVSuggestionSerializer, Conflict, ConflictSerializer, \
    ResolveConflictSerializer, StudentSerializer, CoachSerializer, ProjectSerializer, \
    ProjectGetSerializer, SkillSerializer, SuggestionSerializer, ProjectSuggestionSerializer, \
    UpdateCoachSerializer, RemoveProjectSuggestionSerializer, SentEmailSerializer
from .models import RequiredSkills, Student, Coach, Skill, Project, SentEmail, Suggestion, ProjectSuggestion
from .tally.tally import TallyForm
from .permissions import IsAdmin, IsOwnerOrAdmin, IsActive


class StudentViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    API endpoint that allows students to be viewed, edited or searched.

    - Search students with ?search=string query parameter.
    - Filter students with the following query parameters:
        * ?alum=[true, false]
        * ?language=string
        * ?skills=:id:
        * ?student_coach=[true, false]
        * ?english_rating=[1-5]
        * ?status=[0-5]
        * ?on_project=[true, false]
        * ?suggested_by_user=[true, false]
        * ?suggestion=[yes, no, maybe, none, 0, 1, 2, 3]
    - Use a specific page size with ?page_size=[1-500] query parameter.
    - Sort students with the ?ordering=[first_name, last_name, email, status] query parameter.
        * Use ?ordering=-... to sort in descending order

    Example queries:

        /api/students/?search=Jan
        /api/students/?alum=true&status=0&skills=1&suggestion=yes&on_project=true&language=Dutch
        /api/students/?page_size=2
        /api/students/?ordering=last_name
    """
    # filter final decision out of suggestions
    queryset = Student.objects.prefetch_related(
        Prefetch('suggestion_set',
                 queryset=Suggestion.objects.filter(final=False),
                 to_attr='filtered_suggestions')
    ).order_by('id')
    pagination_class = StandardPagination
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsActive]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend,
                       StudentOnProjectFilter, StudentSuggestedByUserFilter,
                       StudentFinalDecisionFilter, ]
    search_fields = ['first_name', 'last_name', 'call_name', 'email', 'degree',
                     'studies', 'motivation', 'school_name', 'employment_agreement', 'hinder_work']
    filterset_fields = ['alum', 'language', 'skills',
                        'student_coach', 'english_rating', 'status']
    ordering_fields = ['first_name', 'last_name', 'email', 'status']

    @action(detail=True, methods=['post'], serializer_class=SuggestionSerializer)
    def make_suggestion(self, request, pk=None):
        """
        let a coach make a suggestion for the current student
        if the coach has already made a suggestion for this student, it is updated
        returns HTTP response:
            400 BAD REQUEST: there was required data missing or the data could not be serialized
            201 CREATED:     a new suggestion was created or updated
        """
        serializer = SuggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            # save suggestion
            serializer.save(student=self.get_object(),
                            coach=request.user, final=False)

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
        serializer = SuggestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            student = self.get_object()
            # save suggestion
            suggestion = serializer.save(
                student=student, coach=request.user, final=True)
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
                    'type': 'final_decision',
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
                'type': 'remove_final_decision',
                'data': {
                    'student_id': pk
                }
            }
        )

        return Response(status=(status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND))

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def tallyregistration(self, request, pk=None):  # pylint: disable=no-self-use,unused-argument
        """
        Endpoint to which Tally's webhook can connect to register students.
        returns HTTP response:
            400 BAD REQUEST:  The request data was malformatted or a student tried to register twice
            201 CREATED:    The student registration resulted in a new student being created
        """
        tally = TallyForm.from_file()
        try:
            form = tally.transform(tally.validate(request.data))
            skill_names = form.pop("skills")
            student = Student.objects.create(**form)
            skills = []
            for skill_name in skill_names:
                existing_skill = Skill.objects.filter(name=skill_name).first()
                if existing_skill is None:
                    skills.append(Skill.objects.create(
                        name=skill_name, color="grey"))
                else:
                    skills.append(existing_skill)
            student.skills.set(skills)
        except Exception as exc:  # pylint: disable=broad-except
            return Response(str(exc), status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], serializer_class=BulkStatusSerializer)
    def bulk_status(self, request):  # pylint: disable=no-self-use
        """
        endpoint to change the status of multiple students at once (in bulk)
        expects a status and a list of students
        returns HTTP response:
            400 BAD REQUEST:    there was required data missing or the data could not be serialized
            200 OK              the status of all given students was changed
        """
        serializer = BulkStatusSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            for student in serializer.validated_data['students']:
                student.status = serializer.validated_data['status']
                student.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
    def export_csv(self, request):
        """
        endpoint to export students information to csv
        returns a HTTP response with a zip file containing the following files:
            students.csv
            suggestions.csv
        """
        students = export_to_csv(self.get_queryset(), 'students', CSVStudentSerializer)
        suggestions = export_to_csv(Suggestion.objects.all().order_by('id'), 'suggestions', CSVSuggestionSerializer)
        return create_zipfile_response('student', [students, suggestions])


class CoachViewSet(viewsets.GenericViewSet,  # pylint: disable=too-many-ancestors
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):  # No create, this is handled in RegisterView
    """
    API endpoint that allows coaches to be viewed, edited or searched.

    Remarks:

    A coach cannot be created using this (API) endpoint.
    A coach can only update and view his/her own data, only
    admins can update and view all data.

    - Search coaches with ?search=string query parameter.
    - Filter coaches with the following query parameters:
        * ?is_admin=[true, false]
        * ?is_active=[true, false]
    - Use a specific page size with ?page_size=[1-500] query parameter.
    - Sort coaches with the ?ordering=[first_name, last_name, email, is_admin, is_active] query parameter.
        * Use ?ordering=-... to sort in descending order

    Example queries:

        /api/coaches/?is_admin=false&is_active=true
        /api/coaches/?search=Cattoire
        /api/coaches/?page_size=10
        /api/coaches/?ordering=last_name
    """
    queryset = Coach.objects.all().order_by('id')
    pagination_class = StandardPagination
    serializer_class = CoachSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsOwnerOrAdmin, IsActive]
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'email']
    filterset_fields = ['is_admin', 'is_active']
    ordering_fields = ['first_name', 'last_name',
                       'email', 'is_admin', 'is_active']

    # pylint: disable=unused-argument,arguments-differ
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
    def update_status(self, request, pk=None):  # pylint: disable=unused-argument
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
                coach.is_admin = serializer.data.get(
                    'is_admin', coach.is_admin)
                coach.is_active = serializer.data.get(
                    'is_active', coach.is_active)
                coach.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "you can not update your own admin status"}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
    def export_csv(self, request):
        """
        endpoint to export coach information to csv
        returns a HTTP response with a zip file containing the following files:
            coaches.csv
        """
        coaches = export_to_csv(self.get_queryset(), 'coaches', CSVCoachSerializer)
        return create_zipfile_response('coach', [coaches])


class ProjectViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    API endpoint that allows projects to be viewed, edited or searched.

    Remark:

    Only admins can access this (API) endpoint, coaches can just
    add or remove student suggestions.

    - Search projects with ?search=string query parameter.
    - Filter projects with the following query parameters:
        * ?required_skills=:id:,
        * ?coaches=:id:,
        * ?suggested_students=:id:
    - Use a specific page size with ?page_size=[1-500] query parameter.
    - Sort projects with the ?ordering=[name, partner_name] query parameter.
        * Use ?ordering=-... to sort in descending order

    Example queries:

        /api/projects/?required_skills=1&coaches=2&suggested_students=1
        /api/projects/?ordering=name,-partner_name
    """
    queryset = Project.objects.all().order_by('id')
    pagination_class = StandardPagination
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin, IsActive]
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'partner_name', 'extra_info']
    filterset_fields = ['required_skills', 'coaches', 'suggested_students']
    ordering_fields = ['name', 'partner_name']

    def get_serializer_class(self):
        """
        override method to change serializer class in list and retrieve (GET) requests
        this way more coach information can be returned in project responses,
        but not needed when making POST, PUT, PATCH requests
        """
        if hasattr(self, 'action') and self.action == 'list' or self.action == 'retrieve':
            return ProjectGetSerializer
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
        serializer = ProjectSuggestionSerializer(
            data=request.data, context={'request': request})
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
    def get_conflicting_projects(self, request):  # pylint: disable=no-self-use
        """
        get a list of conflicting projects;
        two projects are conflicting if one student has been suggested/assigned to both of them
        returns HTTP response:
            200 OK: a list of conflicts was returned
        """
        students = Student.objects.all()
        conflicts = []
        # loop over students
        for student in students:
            # get all projectsuggestions with current student
            projectsuggestions = ProjectSuggestion.objects.filter(
                student=student)
            # check if student is suggested/assigned to more than 1 project
            if projectsuggestions.count() > 1:
                # get projects out of projectsuggestions
                projects = Project.objects.filter(
                    id__in=projectsuggestions.values_list('project', flat=True))
                # create Conflict object and add it to the list
                conflicts.append(Conflict(student, projects))

        # paginate response
        page = self.paginate_queryset(conflicts)
        serializer = ConflictSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['post'], serializer_class=ResolveConflictSerializer,
            permission_classes=[permissions.IsAuthenticated, IsActive])
    def resolve_conflicts(self, request):  # pylint: disable=no-self-use
        """
        let a coach resolve conflicts
        exptects a list of objects with a student, project, coach and skill,
        this will remove all projectsuggestions that conflict with the given objects
        returns HTTP response:
            204 NO CONTENT: all conflicting projectsuggestions have been deleted
            400 BAD REQUEST: there was required data missing or the students were not unique
        """
        serializer = ResolveConflictSerializer(
            data=request.data, many=True, context={'request': request})
        if serializer.is_valid():
            # check if all students are unique
            students = [ps['student'] for ps in serializer.validated_data]
            if len(students) == len(set(students)):
                # loop over projectsuggestions
                for projectsuggestion in serializer.validated_data:
                    # delete all projectsuggestions with the current student, except the one given
                    ProjectSuggestion.objects\
                        .filter(student=projectsuggestion['student'])\
                        .exclude(**projectsuggestion)\
                        .delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "students must be unique"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
    def export_csv(self, request):
        """
        endpoint to export project information to csv
        returns a HTTP response with a zip file containing the following files:
            projects.csv
            required_skills.csv
            suggested_students.csv
        """
        projects = export_to_csv(self.get_queryset(), 'projects', CSVProjectSerializer)
        required_skills = export_to_csv(RequiredSkills.objects.all(), 'required_skills', CSVRequiredSkillSerializer)
        suggested_students = export_to_csv(ProjectSuggestion.objects.all(), 'suggested_students', CSVProjectSuggestionSerializer)
        return create_zipfile_response('project', [projects, required_skills, suggested_students])


class SkillViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    API endpoint that allows skills to be viewed, edited or searched.

    - Search skills with ?search=string query parameter.
    - Use a specific page size with ?page_size=[1-500] query parameter.
    - Sort skills with the ?ordering=name query parameter.
        * Use ?ordering=-... to sort in descending order

    Example queries:

        /api/skills/?search=Back-end Developer
        /api/skills/?ordering=name
    """
    queryset = Skill.objects.all().order_by('id')
    pagination_class = StandardPagination
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated, IsActive]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    # pylint: disable=unused-argument,arguments-differ
    def destroy(self, request, pk=None):
        if request.user.is_admin:
            try:
                self.perform_destroy(self.get_object())
            except RestrictedError:
                return Response({"detail": "can't delete skill, it is used in at least one project suggestion"},
                                status=status.HTTP_403_FORBIDDEN)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
    def export_csv(self, request):
        """
        endpoint to export skill information to csv
        returns a HTTP response with a zip file containing the following files:
            skills.csv
        """
        skills = export_to_csv(self.get_queryset(), 'skills', CSVSkillSerializer)
        return create_zipfile_response('skill', [skills])


class SentEmailViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    API endpoint that allows sent emails to be viewed, edited or searched.

    - Search emails with ?search=string query parameter.
    - Filter emails with the following query parameters:
        * ?sender=:id:,
        * ?receiver=:id:,
        * ?date=yyyy-mm-dd,
        * ?before=yyyy-mm-ddThh:mm:ss,
        * ?after=yyyy-mm-ddThh:mm:ss
    - Use a specific page size with ?page_size=[1-500] query parameter.
    - Sort emails with the ?ordering=[time, sender, receiver] query parameter.
        * Use ?ordering=-... to sort in descending order
        * sender and receiver are sorted using id

    Example queries:

        /api/emails/?sender=1&after=2022-04-03
        /api/emails/?ordering=time,-sender
    """
    queryset = SentEmail.objects.all().order_by('id')
    pagination_class = StandardPagination
    serializer_class = SentEmailSerializer
    permission_classes = [permissions.IsAuthenticated, IsActive]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,
                       DjangoFilterBackend, EmailDateTimeFilter]
    search_fields = ['info']
    filterset_fields = ['sender', 'receiver']
    ordering_fields = ['time', 'sender', 'receiver']

    # pylint: disable=arguments-differ
    def create(self, request):
        serializer = SentEmailSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsActive, IsAdmin])
    def export_csv(self, request):
        """
        endpoint to export email information to csv
        returns a HTTP response with a zip file containing the following files:
            emails.csv
        """
        emails = export_to_csv(self.get_queryset(), 'emails', CSVSentEmailSerializer)
        return create_zipfile_response('email', [emails])


class GithubLogin(SocialLoginView):
    """
    Github login view.
    """
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://0.0.0.0:8000/accounts/github/login/callback/"
    client_class = OAuth2Client


class CustomRegisterView(RegisterView):
    """
    This class overrides the registerview of rest_auth so users that get registered don't automatically
    get logged in.
    """
    permission_classes = [permissions.IsAuthenticated, IsActive, IsAdmin]

    def get_response_data(self, user):
        return {'detail': ('User has been created.')}

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user
