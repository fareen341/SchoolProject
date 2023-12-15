from rest_framework import viewsets
from .models import Student, Parent, DocumentUpload
from .serializers import StudentSerializers, ParentSerializers, DocumentUploadSerializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView


# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["admission_category", "class_name", "section"]
    search_filter = ["admission_category", "class_name", "section"]


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["student"]
    search_filter = ["student"]


class DocumentUploadViewSet(viewsets.ModelViewSet):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["student"]



class Enroll(CreateView):
    model = Student
    fields = '__all__'
    success_url = 'success'


class SuccessView(TemplateView):
    template_name = 'enroll/success.html'
