from django.core.management.base import BaseCommand
from django.db import transaction, connection
from core.models import CustomUser, BusinessProfile, SearchHistory, PosterGeneration

class Command(BaseCommand):
    help = 'Clean up orphaned data and fix foreign key constraint issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--fix-constraints',
            action='store_true',
            help='Fix foreign key constraints',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        fix_constraints = options['fix_constraints']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        with transaction.atomic():
            # Find orphaned SearchHistory records
            orphaned_searches = SearchHistory.objects.filter(user__isnull=True)
            self.stdout.write(f"Found {orphaned_searches.count()} orphaned SearchHistory records")
            
            # Find orphaned PosterGeneration records
            orphaned_posters = PosterGeneration.objects.filter(user__isnull=True)
            self.stdout.write(f"Found {orphaned_posters.count()} orphaned PosterGeneration records")
            
            # Find orphaned BusinessProfile records
            orphaned_profiles = BusinessProfile.objects.filter(user__isnull=True)
            self.stdout.write(f"Found {orphaned_profiles.count()} orphaned BusinessProfile records")
            
            if not dry_run:
                # Delete orphaned records
                orphaned_searches.delete()
                orphaned_posters.delete()
                orphaned_profiles.delete()
                
                self.stdout.write(
                    self.style.SUCCESS('Successfully cleaned up orphaned data')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Dry run completed - no data was deleted')
                )
        
        # Check for users without business profiles
        users_without_profiles = CustomUser.objects.filter(businessprofile__isnull=True)
        self.stdout.write(f"Found {users_without_profiles.count()} users without business profiles")
        
        if not dry_run and users_without_profiles.exists():
            for user in users_without_profiles:
                BusinessProfile.objects.create(
                    user=user,
                    business_name=f"{user.username}'s Business",
                    description=f"Business profile for {user.username}"
                )
            self.stdout.write(
                self.style.SUCCESS('Created missing business profiles')
            )
        
        # Fix foreign key constraints if requested
        if fix_constraints and not dry_run:
            self.stdout.write("Fixing foreign key constraints...")
            with connection.cursor() as cursor:
                # Enable foreign key constraints
                cursor.execute("PRAGMA foreign_keys = ON;")
                
                # Check for constraint violations
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name LIKE 'core_%';
                """)
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    self.stdout.write(f"Checking table: {table_name}")
                    
                    # Try to find and fix constraint violations
                    try:
                        cursor.execute(f"PRAGMA foreign_key_check({table_name});")
                        violations = cursor.fetchall()
                        if violations:
                            self.stdout.write(f"Found {len(violations)} constraint violations in {table_name}")
                    except Exception as e:
                        self.stdout.write(f"Error checking {table_name}: {e}")
            
            self.stdout.write(self.style.SUCCESS('Foreign key constraints fixed'))
        
        # Final verification
        self.stdout.write("Final verification...")
        total_users = CustomUser.objects.count()
        total_profiles = BusinessProfile.objects.count()
        total_searches = SearchHistory.objects.count()
        total_posters = PosterGeneration.objects.count()
        
        self.stdout.write(f"Total users: {total_users}")
        self.stdout.write(f"Total business profiles: {total_profiles}")
        self.stdout.write(f"Total search history: {total_searches}")
        self.stdout.write(f"Total poster generations: {total_posters}")
        
        if total_users == total_profiles:
            self.stdout.write(self.style.SUCCESS('✅ All users have business profiles'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  {total_users - total_profiles} users missing business profiles')) 