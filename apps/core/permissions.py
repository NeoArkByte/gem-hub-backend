from rest_framework import permissions
from .models import Profile  # Adjust this import path to your Profile model

def IsOwner(field_name='owner'):  # Changed default from 'user' to 'owner' to match your model
    """
    A Permission Factory that generates a custom permission class 
    checking ownership based on a dynamically provided field name string.
    Works seamlessly with the lightweight in-memory SupabaseUser class.
    """
    class DynamicIsOwner(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            if not request.user or not request.user.is_authenticated:
                return False
                
            try:
                clean_auth_id = str(request.user.id).strip('\'"“” ')
                        
                user_profile = Profile.objects.get(profile_id=clean_auth_id)
                
                obj_owner_profile = getattr(obj, field_name, None)
                
                print("--- Django Ownership Check Debug ---")
                print(f"Target Object: {obj}")
                print(f"Object Owner Profile (Evaluated String): {obj_owner_profile}")
                print(f"Requesting User Profile (Evaluated String): {user_profile}")
                
                obj_owner_pk = getattr(obj_owner_profile, 'pk', None)
                request_user_pk = getattr(user_profile, 'pk', None)
                print(f"Comparing PKs -> Gem Owner PK: {obj_owner_pk} == Request User PK: {request_user_pk}")
                print("------------------------------------")
                
                return obj_owner_profile == user_profile

            except (Profile.DoesNotExist, AttributeError) as e:
                print(f"Ownership check failed or profile not found: {str(e)}")
                return False

    return DynamicIsOwner



class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to check if the Supabase JWT payload contains an admin role.
    Operates purely in-memory using the SupabaseUser object.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        clean_auth_id = str(request.user.id).strip('\'"“” ')
        user_profile = Profile.objects.get(profile_id=clean_auth_id)

        user_role = getattr(user_profile, 'role', '')

        print("--- Supabase JWT Admin Check ---")
        print(f"JWT Role Claim: '{user_role}'")
        print("--------------------------------")

        return str(user_role).lower() == 'admin'