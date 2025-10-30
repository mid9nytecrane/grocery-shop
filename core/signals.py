from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings 

from .models import Profile
import logging 

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User, dispatch_uid="create_user_profile")
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            )
        print(f"\nprofile created for {instance.username}")


#@receiver(post_save, sender=User, dispatch_uid="save_user_profile")
# def save_user_profile(sender,created,instance, **kwargs):
#     instance.profile.save()


@receiver(post_save,sender=User,dispatch_uid="send_welcome_email")
def send_welcome_user(sender, instance, created, **kwargs):
    """ send welcome to users after signing up"""
    print('fired signal!!!')
    print(f"logger: {logger}")

    if created:
        try:
            logger.info(f"Welcome, email would be sent to: {instance.email}")
            send_mail(
                'Welcome !',
                'Thanks for signing up',
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Error in send_welcome_user: {e}")
