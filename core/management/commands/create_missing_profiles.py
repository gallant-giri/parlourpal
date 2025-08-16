from django.core.management.base import BaseCommand
from core.models import CustomUser, BusinessProfile

class Command(BaseCommand):
    help = 'Create business profiles for users who don\'t have them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Create profile for specific username',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Create profiles for all users without profiles',
        )

    def handle(self, *args, **options):
        if options['username']:
            try:
                user = CustomUser.objects.get(username=options['username'])
                if not hasattr(user, 'businessprofile'):
                    profile = BusinessProfile.objects.create(
                        user=user,
                        business_name=f"{user.username}'s Business",
                        description=f"Business profile for {user.username}"
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Created business profile for {user.username}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'User {user.username} already has a business profile')
                    )
            except CustomUser.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User {options["username"]} does not exist')
                )
        
        elif options['all']:
            users_without_profiles = CustomUser.objects.filter(businessprofile__isnull=True)
            created_count = 0
            
            for user in users_without_profiles:
                profile = BusinessProfile.objects.create(
                    user=user,
                    business_name=f"{user.username}'s Business",
                    description=f"Business profile for {user.username}"
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created business profile for {user.username}')
                )
            
            self.stdout.write(
                self.style.SUCCESS(f'Created {created_count} business profiles')
            )
        
        else:
            users_without_profiles = CustomUser.objects.filter(businessprofile__isnull=True)
            if users_without_profiles.exists():
                self.stdout.write('Users without business profiles:')
                for user in users_without_profiles:
                    self.stdout.write(f'  - {user.username} (ID: {user.id})')
                self.stdout.write('\nRun with --all to create profiles for all users')
            else:
                self.stdout.write(
                    self.style.SUCCESS('All users have business profiles!')
                ) 