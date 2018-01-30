from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.models import *
from main import models
from django.contrib.auth.models import User

from allauth.exceptions import ImmediateHttpResponse
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class AccountAdapter(DefaultAccountAdapter):


    def get_login_redirect_url(self, request):
        obj = SocialAccount.objects.get(user=request.user)
        try:
        	profile = obj.user.profile
        except Exception:
        	profile, created = \
        		models.Profile.objects.get_or_create(user=request.user)
        if obj.extra_data.get('email'):
        	profile.email = obj.extra_data.get('email')
        if obj.extra_data.get('name'):
        	profile.name = obj.extra_data.get('name')
        if obj.extra_data.get('gender'):
            if obj.extra_data.get('gender') == "male":
                profile.gender = "M"
            else:
                profile.gender = "F"
        profile.save()

        return request.session.get("next")

  # def get_logout_redirect_url(self, request):
  #     return "/"