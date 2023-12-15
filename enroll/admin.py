from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Student, Parent, DocumentUpload
from .resources import StudentResource, ParentResource, DocumentUploadResource
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter


class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = [
        'name', 'gender', 'aadhar_card_number', 'dob', 'identification_marks', 'admission_category',
        'height', 'weight', 'mail_id', 'contact_detail', 'address', 'enrollment_id', 'class_name',
        'section', 'doj'
    ]
    list_filter = ("admission_category", "class_name", "section")
    search_fields = ("admission_category", "class_name", "section")
    list_per_page = 20


class ParentAdmin(ImportExportModelAdmin):
    resource_class = ParentResource
    list_display = [
        'student', 'father_name', 'father_qualification', 'father_profession',
        'father_designation', 'father_aadhar_card', 'father_mobile_number',
        'father_mail_id', 'mother_name', 'mother_qualification', 'mother_profession',
        'mother_designation', 'mother_aadhar_card', 'mother_mobile_number',
        'mother_mail_id'
    ]
    list_per_page = 20
    list_filter = ("student",)


class DocumentUploadAdmin(ImportExportModelAdmin):
    resource_class = DocumentUploadResource
    list_display = ['student', 'document']
    list_per_page = 20
    list_filter = ("student",)


admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(DocumentUpload, DocumentUploadAdmin)
