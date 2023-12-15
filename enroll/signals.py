from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=Student)
def send_custom_email(sender, **kwargs):
    instance = kwargs["instance"]
    if getattr(instance, "dry_run", False):
        return
    else:
        try:
            subject = 'Enrollment Successful.'
            message_student = mark_safe(f"""
            <p>Dear {instance.name},</p>
            <p>You got enroll in Dummy School your Enrollment ID is <strong>{instance.enrollment_id}</strong>
            let’s provide us the hard documents for thr future references.</p>
            <p>Team</p>
            <p>Dummy School</p>
            """)
            from_email = 'fareenansari33@gmail.com'
            recipient_list = [instance.mail_id]
            send_mail(subject, message_student, from_email, recipient_list, html_message=message_student)

            message_admin = mark_safe(f"""
            <p>Dear Admin,</p>
            <p>You got a new student <strong>{instance.name}</strong> enrolled in class <strong>{instance.class_name}</strong>,
            section <strong>{instance.section}</strong> with enrollment id <strong>{instance.enrollment_id}</strong> in this session.</p>
            <p>Bot Msg.</p>
            """)
            recipient_list = ["durganand.jha@habrie.com"]
            send_mail(subject, message_admin, from_email, recipient_list, html_message=message_admin)
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


# Authentication Code
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)