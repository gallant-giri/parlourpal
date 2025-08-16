from django.core.management.base import BaseCommand
from core.models import BusinessProfile
from core.cloudinary_utils import upload_file_to_cloudinary
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Migrate all local BusinessProfile images to Cloudinary and update image_url.'

    def handle(self, *args, **options):
        migrated = 0
        for profile in BusinessProfile.objects.all():
            if profile.image and not profile.image_url:
                local_path = profile.image.path
                if os.path.exists(local_path):
                    self.stdout.write(f'Migrating {local_path}...')
                    result = upload_file_to_cloudinary(local_path, folder="logos", public_id=f"logo_{profile.user.username}")
                    if result['success']:
                        profile.image_url = result['url']
                        profile.save()
                        migrated += 1
                        self.stdout.write(self.style.SUCCESS(f'Uploaded to Cloudinary: {result["url"]}'))
                        # Optionally remove local file
                        # os.remove(local_path)
                    else:
                        self.stdout.write(self.style.ERROR(f'Failed: {result["error"]}'))
        self.stdout.write(self.style.SUCCESS(f'Migrated {migrated} images to Cloudinary.')) 