from rest_framework import authentication
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate

User = get_user_model()


class DevAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        # qs = User.objects.all()
        qs = User.objects.filter(id=1)
        user = qs.order_by("?").first()
        return (user, None)
