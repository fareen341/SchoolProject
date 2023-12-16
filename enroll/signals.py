from django.dispatch import receiver
from .models import Student
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from .tasks import send_custom_email


@receiver(post_save, sender=Student)
def send_custom_email_wrapper(sender, **kwargs):
    instance = kwargs["instance"]
    if getattr(instance, "dry_run", False):
        return
    else:
        instance_data = {
            'name': instance.name,
            'enrollment_id': instance.enrollment_id,
            'mail_id': instance.mail_id,
            'class_name': instance.class_name,
            'section': instance.section,
        }
        send_custom_email.delay(instance_data)


# Authentication Code
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)