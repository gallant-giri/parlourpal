from django.contrib import admin
from .models import CustomUser, BusinessProfile, SearchHistory, PosterGeneration, Festival, UserHistory
from django.contrib.auth.admin import UserAdmin
from django.db import transaction
from django.contrib import messages

class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'location', 'phone')
    list_filter = ('location',)
    search_fields = ('business_name', 'user__username', 'user__email', 'location')
    readonly_fields = ('user',)  # ✅ prevents changing user
    actions = ['fix_database_issues']
    
    def get_queryset(self, request):
        """Filter out any problematic records and handle errors gracefully"""
        try:
            qs = super().get_queryset(request)
            # Only show records with valid user references
            return qs.filter(user__isnull=False)
        except Exception as e:
            # If there's an error, try to fix it automatically
            print(f"Error in BusinessProfile queryset: {e}")
            try:
                # Try to clean up orphaned records automatically
                from django.db import transaction
                with transaction.atomic():
                    # Delete orphaned records
                    BusinessProfile.objects.filter(user__isnull=True).delete()
                    SearchHistory.objects.filter(user__isnull=True).delete()
                    PosterGeneration.objects.filter(user__isnull=True).delete()
                    
                    # Create missing business profiles
                    users_without_profiles = CustomUser.objects.filter(businessprofile__isnull=True)
                    for user in users_without_profiles:
                        BusinessProfile.objects.create(
                            user=user,
                            business_name=f"{user.username}'s Business",
                            description=f"Business profile for {user.username}"
                        )
                
                # Try the queryset again
                qs = super().get_queryset(request)
                return qs.filter(user__isnull=False)
            except Exception as fix_error:
                print(f"Auto-fix failed: {fix_error}")
                return BusinessProfile.objects.none()
    
    def changelist_view(self, request, extra_context=None):
        """Override changelist view to handle errors gracefully"""
        try:
            return super().changelist_view(request, extra_context)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Error loading business profiles: {str(e)}")
            # Return a simple view with error message
            from django.shortcuts import render
            context = {
                'title': 'Business Profiles',
                'error_message': f"Database error: {str(e)}. Please run the cleanup command.",
            }
            return render(request, 'admin/core/businessprofile/error.html', context)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None:  # Creating new profile
            # Only show users who don't already have a business profile
            form.base_fields['user'].queryset = CustomUser.objects.filter(businessprofile__isnull=True)
        return form
    
    def save_model(self, request, obj, form, change):
        # Ensure the user doesn't already have a profile
        if not change and BusinessProfile.objects.filter(user=obj.user).exists():
            self.message_user(request, f"User {obj.user.username} already has a business profile.", level='ERROR')
            return
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        """Custom delete method to handle cascade deletion properly"""
        try:
            # Delete related objects first
            SearchHistory.objects.filter(user=obj.user).delete()
            PosterGeneration.objects.filter(user=obj.user).delete()
            # Then delete the business profile
            obj.delete()
            self.message_user(request, f"Business profile for {obj.user.username} deleted successfully.")
        except Exception as e:
            self.message_user(request, f"Error deleting business profile: {str(e)}", level='ERROR')
    
    def delete_queryset(self, request, queryset):
        """Handle bulk deletion"""
        for obj in queryset:
            self.delete_model(request, obj)
    
    def fix_database_issues(self, request, queryset):
        """Admin action to fix database issues"""
        try:
            from django.db import transaction
            with transaction.atomic():
                # Delete orphaned records
                orphaned_profiles = BusinessProfile.objects.filter(user__isnull=True)
                orphaned_searches = SearchHistory.objects.filter(user__isnull=True)
                orphaned_posters = PosterGeneration.objects.filter(user__isnull=True)
                
                orphaned_profiles.delete()
                orphaned_searches.delete()
                orphaned_posters.delete()
                
                # Create missing business profiles
                users_without_profiles = CustomUser.objects.filter(businessprofile__isnull=True)
                for user in users_without_profiles:
                    BusinessProfile.objects.create(
                        user=user,
                        business_name=f"{user.username}'s Business",
                        description=f"Business profile for {user.username}"
                    )
            
            self.message_user(request, f"Database issues fixed! Deleted {orphaned_profiles.count()} orphaned profiles, {orphaned_searches.count()} orphaned searches, {orphaned_posters.count()} orphaned posters, and created {users_without_profiles.count()} missing business profiles.")
        except Exception as e:
            self.message_user(request, f"Error fixing database: {str(e)}", level='ERROR')
    
    fix_database_issues.short_description = "Fix database issues (delete orphaned records and create missing profiles)"

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'email_verified')
    list_filter = ('is_staff', 'is_superuser', 'email_verified', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    actions = ['safe_delete_users']
    
    def delete_model(self, request, obj):
        """Custom delete method to ensure all related data is deleted"""
        try:
            # Delete all related data first
            SearchHistory.objects.filter(user=obj).delete()
            PosterGeneration.objects.filter(user=obj).delete()
            # BusinessProfile will be deleted automatically due to CASCADE
            obj.delete()
            self.message_user(request, f"User {obj.username} and all related data deleted successfully.")
        except Exception as e:
            self.message_user(request, f"Error deleting user: {str(e)}", level='ERROR')
    
    def delete_queryset(self, request, queryset):
        """Handle bulk deletion"""
        for obj in queryset:
            self.delete_model(request, obj)

class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_query', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'search_query')
    readonly_fields = ('created_at',)

class PosterGenerationAdmin(admin.ModelAdmin):
    list_display = ('user', 'promotion_name', 'offer_type', 'created_at')
    list_filter = ('created_at', 'offer_type')
    search_fields = ('user__username', 'promotion_name')
    readonly_fields = ('created_at', 'poster_url')

class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'notification_days', 'is_active', 'created_at')
    list_filter = ('is_active', 'date', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)

class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'created_at', 'is_image_action', 'is_text_action')
    list_filter = ('action_type', 'created_at', 'user')
    search_fields = ('user__username', 'user__email', 'output_data')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def is_image_action(self, obj):
        return obj.is_image_action
    is_image_action.boolean = True
    is_image_action.short_description = 'Image Action'
    
    def is_text_action(self, obj):
        return obj.is_text_action
    is_text_action.boolean = True
    is_text_action.short_description = 'Text Action'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BusinessProfile, BusinessProfileAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)
admin.site.register(PosterGeneration, PosterGenerationAdmin)
admin.site.register(Festival, FestivalAdmin)
admin.site.register(UserHistory, UserHistoryAdmin)
