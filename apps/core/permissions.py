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
            # 1. Block if the user is unauthenticated or anonymous
            if not request.user or not request.user.is_authenticated:
                return False
                
            try:
                # 2. Clean up quotes from the Supabase UUID string stored on our ghost user object
                clean_auth_id = str(request.user.id).strip('\'"“” ')
                        
                # 3. Query your Profile table using that clean UUID string
                user_profile = Profile.objects.get(profile_id=clean_auth_id)
                
                # 4. Dynamically grab the Profile instance relation from the target object (e.g., obj.owner)
                # Note: This returns a full Profile model object, NOT a string ID.
                obj_owner_profile = getattr(obj, field_name, None)
                
                # --- DEBUG PRINTS ---
                print("--- Django Ownership Check Debug ---")
                print(f"Target Object: {obj}")
                print(f"Object Owner Profile (Evaluated String): {obj_owner_profile}")
                print(f"Requesting User Profile (Evaluated String): {user_profile}")
                
                # To see the actual primary keys being compared behind the scenes:
                obj_owner_pk = getattr(obj_owner_profile, 'pk', None)
                request_user_pk = getattr(user_profile, 'pk', None)
                print(f"Comparing PKs -> Gem Owner PK: {obj_owner_pk} == Request User PK: {request_user_pk}")
                print("------------------------------------")
                # --------------------

                # 5. Compare the target object's Profile model instance directly to our fetched Profile model instance
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
        # 1. Block if the user is unauthenticated or anonymous
        if not request.user or not request.user.is_authenticated:
            return False
        
        clean_auth_id = str(request.user.id).strip('\'"“” ')
        user_profile = Profile.objects.get(profile_id=clean_auth_id)

        # 2. Extract the role directly from your in-memory SupabaseUser object
        user_role = getattr(user_profile, 'role', '')

        # --- DEBUG PRINT ---
        print("--- Supabase JWT Admin Check ---")
        print(f"JWT Role Claim: '{user_role}'")
        print("--------------------------------")

        # 3. Check if the role matches your admin string (case-insensitive)
        return str(user_role).lower() == 'admin'