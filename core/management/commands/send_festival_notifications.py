from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from core.models import Festival, CustomUser
from core.email_utils import send_festival_notification_email

class Command(BaseCommand):
    help = 'Send festival notifications to verified users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Test mode - show what would be sent without actually sending',
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['pre', 'festival-day', 'both'],
            default='both',
            help='Type of notifications to send',
        )

    def handle(self, *args, **options):
        today = date.today()
        test_mode = options['test']
        notification_type = options['type']
        
        self.stdout.write(f"🎊 Festival Notification System")
        self.stdout.write(f"Date: {today}")
        self.stdout.write(f"Mode: {'TEST' if test_mode else 'LIVE'}")
        self.stdout.write(f"Type: {notification_type}")
        self.stdout.write("-" * 50)
        
        # Get active festivals
        active_festivals = Festival.objects.filter(is_active=True)
        
        if not active_festivals.exists():
            self.stdout.write(self.style.WARNING("No active festivals found."))
            return
        
        # Get verified users with notifications enabled
        users = CustomUser.objects.filter(
            email_verified=True,
            notifications_enabled=True
        )
        
        if not users.exists():
            self.stdout.write(self.style.WARNING("No verified users with notifications enabled."))
            return
        
        self.stdout.write(f"Found {active_festivals.count()} active festivals")
        self.stdout.write(f"Found {users.count()} users to notify")
        
        notifications_sent = 0
        
        for festival in active_festivals:
            self.stdout.write(f"\n📅 Processing: {festival.name} ({festival.date})")
            
            # Check for pre-festival notifications
            if notification_type in ['pre', 'both']:
                pre_notification_date = festival.notification_date
                if today == pre_notification_date:
                    self.stdout.write(f"  ✅ Pre-festival notification due today!")
                    if not test_mode:
                        for user in users:
                            try:
                                if send_festival_notification_email(user, festival, 'pre'):
                                    notifications_sent += 1
                                    self.stdout.write(f"    📧 Sent to {user.email}")
                                else:
                                    self.stdout.write(f"    ❌ Failed to send to {user.email}")
                            except Exception as e:
                                self.stdout.write(f"    ❌ Error sending to {user.email}: {e}")
                    else:
                        self.stdout.write(f"    🧪 TEST: Would send to {users.count()} users")
                        notifications_sent += users.count()
                else:
                    days_until = (pre_notification_date - today).days
                    if days_until > 0:
                        self.stdout.write(f"  ⏰ Pre-notification in {days_until} days")
                    else:
                        self.stdout.write(f"  ⏰ Pre-notification was {abs(days_until)} days ago")
            
            # Check for festival day notifications
            if notification_type in ['festival-day', 'both'] and festival.send_on_festival_day:
                if today == festival.date:
                    self.stdout.write(f"  🎉 Festival day notification due today!")
                    if not test_mode:
                        for user in users:
                            try:
                                if send_festival_notification_email(user, festival, 'festival-day'):
                                    notifications_sent += 1
                                    self.stdout.write(f"    📧 Sent to {user.email}")
                                else:
                                    self.stdout.write(f"    ❌ Failed to send to {user.email}")
                            except Exception as e:
                                self.stdout.write(f"    ❌ Error sending to {user.email}: {e}")
                    else:
                        self.stdout.write(f"    🧪 TEST: Would send to {users.count()} users")
                        notifications_sent += users.count()
                else:
                    days_until = (festival.date - today).days
                    if days_until > 0:
                        self.stdout.write(f"  ⏰ Festival day in {days_until} days")
                    else:
                        self.stdout.write(f"  ⏰ Festival was {abs(days_until)} days ago")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(f"📊 Summary:")
        self.stdout.write(f"  Total notifications: {notifications_sent}")
        self.stdout.write(f"  Mode: {'TEST' if test_mode else 'LIVE'}")
        
        if test_mode:
            self.stdout.write(self.style.SUCCESS("✅ Test completed successfully!"))
        else:
            self.stdout.write(self.style.SUCCESS("✅ Festival notifications sent successfully!")) 