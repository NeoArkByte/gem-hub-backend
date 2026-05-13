import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions

class SupabaseAuth(authentication.BaseAuthentication):
    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token, settings.SUPABASE_JWT_SECRET, 
                algorithms=["HS256"], audience="authenticated"
            )

            # Use Supabase 'sub' (UUID) as the Django username
            user, _ = User.objects.get_or_create(username=payload['sub'])
            return (user, payload)
        
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")
