import uuid
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Festival


def generate_verification_token():
    """Generate a unique verification token"""
    return str(uuid.uuid4())


def send_verification_email(user):
    """Send email verification email to user"""
    try:
        # Generate verification token
        token = generate_verification_token()
        user.verification_token = token
        from django.utils import timezone
        user.token_created_at = timezone.now()
        user.save()
        
        # Create verification URL
        verification_url = f"{settings.SITE_URL}/verify-email/{token}/"
        
        # Email content
        subject = "🎉 Verify Your Email - ParlorPal"
        
        # HTML Email template
        html_message = render_to_string('core/emails/verification_email.html', {
            'user': user,
            'verification_url': verification_url,
            'site_name': 'ParlorPal'
        })
        
        # Plain text version
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return False


def send_festival_notification_email(user, festival, notification_type='pre'):
    """Send festival notification email to user
    
    Args:
        user: CustomUser instance
        festival: Festival instance
        notification_type: 'pre' for pre-festival, 'festival-day' for on festival day
    """
    try:
        if notification_type == 'pre':
            subject = f"🎊 {festival.name} is coming! Time to boost your business!"
            countdown_text = f"Only {festival.notification_days} days to go!"
        else:  # festival-day
            subject = f"🎉 Happy {festival.name}! Special offers for your business!"
            countdown_text = "Today is the day!"
        
        # HTML Email template
        html_message = render_to_string('core/emails/festival_notification.html', {
            'user': user,
            'festival': festival,
            'site_name': 'ParlorPal',
            'notification_type': notification_type,
            'countdown_text': countdown_text
        })
        
        # Plain text version
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        print(f"Error sending festival notification: {e}")
        return False


def send_festival_notification(user, festival):
    """Legacy function - now calls the new function"""
    return send_festival_notification_email(user, festival, 'pre')


def send_festival_notifications():
    """Send festival notifications to all eligible users"""
    from django.utils import timezone
    today = timezone.now().date()
    
    # Get festivals that need notifications today
    festivals = Festival.objects.filter(
        is_active=True
    )
    
    # Filter festivals that need notifications today
    festivals_to_notify = []
    for festival in festivals:
        if festival.notification_date == today:
            festivals_to_notify.append(festival)
    
    if not festivals_to_notify:
        return
    
    # Get users who have verified emails and enabled notifications
    from .models import CustomUser
    eligible_users = CustomUser.objects.filter(
        email_verified=True,
        notifications_enabled=True,
        is_active=True
    )
    
    for festival in festivals_to_notify:
        for user in eligible_users:
            send_festival_notification(user, festival)


def is_token_valid(user, token):
    """Check if verification token is valid and not expired"""
    if user.verification_token != token:
        return False
    
    # Token expires after 24 hours
    if user.token_created_at:
        from django.utils import timezone
        expiration_time = user.token_created_at + timedelta(hours=24)
        if timezone.now() > expiration_time:
            return False
    
    return True 