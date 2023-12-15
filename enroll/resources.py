from import_export import resources
from .models import Student, Parent, DocumentUpload
import re


class NameNotProvidedException(Exception):
    pass


class GenderNotProvidedException(Exception):
    pass


class AadharInvalidException(Exception):
    pass


class AdmissionCategoryNotProvidedException(Exception):
    pass


class StudentResource(resources.ModelResource):
    def before_save_instance(self, instance, using_transactions, dry_run):
        # during 'confirm' step, dry_run is True
        instance.dry_run = dry_run

    class Meta:
        model = Student

    # get all required fields validations here
    def before_import_row(self, row, **kwargs):
        if 'name' not in row or not row['name']:
            raise NameNotProvidedException("The 'name' field is required.")

        if 'gender' not in row or not row['gender']:
            raise GenderNotProvidedException("The 'gender' field is required.")

        # Validate that the gender is in the correct format
        valid_genders = ['FEMALE', 'MALE', 'OTHERS']
        if row['gender'].upper() not in valid_genders:
            raise GenderNotProvidedException("Invalid 'gender' format. Accepted values are 'FEMALE', 'MALE', 'OTHERS'.")

        # Check Aadhar card number validity
        if 'aadhar_card_number' not in row or not row['aadhar_card_number']:
            raise AadharInvalidException("The 'aadhar_card_number' field is required.")

        # Validate Aadhar card number format
        valid_aadhar_regex = '^\d{12}$'
        if not re.match(valid_aadhar_regex, row['aadhar_card_number']):
            raise AadharInvalidException("Invalid Aadhar card number format. It must be exactly 12 digits.")

        if 'admission_category' not in row or not row['admission_category']:
            raise AdmissionCategoryNotProvidedException("The 'admission_category' field is required.")

        # Validate admission category format
        valid_categories = set(category[0] for category in Student._meta.get_field('admission_category').choices)
        if row['admission_category'] not in valid_categories:
            raise AdmissionCategoryNotProvidedException(f"Invalid 'admission_category'. Accepted values are {', '.join(valid_categories)}.")

class ParentResource(resources.ModelResource):
    class Meta:
        model = Parent


class DocumentUploadResource(resources.ModelResource):
    class Meta:
        model = DocumentUpload
