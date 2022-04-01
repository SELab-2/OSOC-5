from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Coach, GithubUser
from django.http import HttpResponse
from allauth.exceptions import ImmediateHttpResponse

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin): 
        try:
            Coach.objects.get(email=sociallogin.user.email)
        except Coach.DoesNotExist:
            raise ImmediateHttpResponse(HttpResponse('No existing email found in the database. Please be sure you already have an account with the same email'))
        coach = Coach.objects.get(email=sociallogin.user.email)
        GithubUser.objects.get_or_create(login=sociallogin.account.extra_data['login'], coach=coach)
        if not sociallogin.is_existing:
            sociallogin.connect(request, coach) 