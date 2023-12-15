from rest_framework import serializers
from .models import Student, Parent, DocumentUpload


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ParentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class DocumentUploadSerializers(serializers.ModelSerializer):
    class Meta:
        model = DocumentUpload
        fields = '__all__'