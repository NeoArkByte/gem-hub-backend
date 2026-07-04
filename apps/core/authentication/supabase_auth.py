import jwt
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
from django.conf import settings
from .supabase_user import SupabaseUser

class SupabaseAuth(authentication.BaseAuthentication):
    
    jwks_client = jwt.PyJWKClient(settings.JWKS_URL)

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        
       
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["ES256"],
                audience="authenticated",
                issuer=f"{settings.SUPABASE_URL}/auth/v1",
            )
            
            print("Decoded JWT payload:", payload)  #
            
            return (SupabaseUser(payload), None)
        
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except (jwt.InvalidTokenError, KeyError, ValueError) as e:
            raise exceptions.AuthenticationFailed(f"Invalid token or key setup: {str(e)}")