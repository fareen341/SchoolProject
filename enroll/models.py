import random
from django.db import models
from django.core.validators import RegexValidator


class Student(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[
        ('FEMALE', 'Female'),
        ('MALE', 'Male'),
        ('OTHERS', 'Other'),
    ])
    aadhar_card_number = models.CharField(max_length=12, validators=[
            RegexValidator(regex='^\d{12}$', message='Adhar card number must be exactly 8 digits.')
        ], verbose_name="Aadhar")
    dob = models.DateField(verbose_name="DOB", help_text="Date of birth.")
    identification_marks = models.TextField()
    admission_category = models.CharField(max_length=50, choices=[
        ('GENERAL', 'General'),
        ('SC', 'Scheduled Caste'),
        ('ST', 'Scheduled Tribe'),
        ('OBC', 'Other Backward Classes'),
        ('EWS', 'Economically Weaker Section'),
        ('DISABLED', 'Physically Disabled'),
        ('MANAGEMENT_QUOTA', 'Management Quota'),
        ('SPORTS_QUOTA', 'Sports Quota'),
        ('FOREIGN_NRI_QUOTA', 'Foreign/NRI Quota'),
        ('MERIT', 'Merit'),
        ('SPECIAL_PROGRAM', 'Special Program'),
    ], verbose_name="Category")
    height = models.PositiveIntegerField(help_text="Height in centimeters")
    weight = models.FloatField()
    mail_id = models.EmailField()
    contact_detail = models.CharField(max_length=20, verbose_name="Contact")
    address = models.TextField()

    enrollment_id = models.CharField(max_length=20, null=True, blank=True, editable=False)
    class_name = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    doj = models.DateField(null=True)
    is_importing = models.BooleanField(editable=False, default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate Enrollment ID
        if not self.enrollment_id:
            enrollment_date_part = self.doj.strftime('%d%m%y')
            student_name_part = self.name[:3].upper()
            random_number_part = f"{random.randint(1, 999):03d}"
            self.enrollment_id = f"{enrollment_date_part}{student_name_part}{random_number_part}"
        super(Student, self).save(*args, **kwargs)


class Parent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=255)
    father_qualification = models.CharField(max_length=100)
    father_profession = models.CharField(max_length=100)
    father_designation = models.CharField(max_length=100)
    father_aadhar_card = models.CharField(max_length=12, validators=[
            RegexValidator(regex='^\d{12}$', message='Adhar card number must be exactly 8 digits.')
        ], verbose_name="Aadhar")
    father_mobile_number = models.CharField(max_length=15)
    father_mail_id = models.EmailField()
    mother_name = models.CharField(max_length=255)
    mother_qualification = models.CharField(max_length=100, null=True, blank=True)
    mother_profession = models.CharField(max_length=100, null=True, blank=True)
    mother_designation = models.CharField(max_length=100, null=True, blank=True)
    mother_aadhar_card = models.CharField(max_length=12, validators=[
            RegexValidator(regex='^\d{12}$', message='Adhar card number must be exactly 8 digits.')
        ], null=True, blank=True, verbose_name="Aadhar")
    mother_mobile_number = models.CharField(max_length=15, null=True, blank=True)
    mother_mail_id = models.EmailField(null=True, blank=True)


class DocumentUpload(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document = models.FileField(upload_to='student_documents/')
