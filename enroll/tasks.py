# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.utils.html import mark_safe


@shared_task
def send_custom_email(instance_data):
    try:
        subject = 'Enrollment Successful.'
        message_student = mark_safe(f"""
        <p>Dear {instance_data['name']},</p>
        <p>You got enrolled in Dummy School. Your Enrollment ID is <strong>{instance_data['enrollment_id']}</strong>
        let’s provide us with the hard documents for future references.</p>
        <p>Team</p>
        <p>Dummy School</p>
        """)
        from_email = 'fareenansari33@gmail.com'
        recipient_list = [instance_data['mail_id']]
        send_mail(subject, message_student, from_email, recipient_list, html_message=message_student)

        message_admin = mark_safe(f"""
        <p>Dear Admin,</p>
        <p>You got a new student <strong>{instance_data['name']}</strong> enrolled in class <strong>{instance_data['class_name']}</strong>,
        section <strong>{instance_data['section']}</strong> with enrollment ID <strong>{instance_data['enrollment_id']}</strong> in this session.</p>
        <p>Bot Msg.</p>
        """)
        recipient_list = ["durganand.jha@habrie.com"]
        send_mail(subject, message_admin, from_email, recipient_list, html_message=message_admin)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False