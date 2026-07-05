from django.contrib.auth.models import AnonymousUser

class SupabaseUser(AnonymousUser):
    """
    A lightweight object that tricks Django into thinking it is a 
    fully implemented User Model, using purely in-memory Supabase JWT data.
    """
    def __init__(self, payload):
        super().__init__()
        self.id = payload.get('sub')          
        self.email = payload.get('email')
        self.role = payload.get('role')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def pk(self):
        return self.id

    def __str__(self):
        return f"SupabaseUser({self.email or self.id})"