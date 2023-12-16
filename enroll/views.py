from rest_framework import viewsets
from .models import Student, Parent, DocumentUpload
from .serializers import StudentSerializers, ParentSerializers, DocumentUploadSerializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.response import Response
from .resources import StudentResource
from django.http import HttpResponse
from tablib import Dataset
from rest_framework import status


class StudentImportExportView(generics.GenericAPIView):
    serializer_class = StudentSerializers
    model_resource = StudentResource

    def get(self, request, *args, **kwargs):
        # Export data
        dataset = self.model_resource().export()
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student_export.csv"'
        return response

    def post(self, request, *args, **kwargs):
        # Import data
        dataset = Dataset()
        file = request.FILES['file']
        imported_data = dataset.load(file.read().decode('utf-8'))
        # Process imported_data and save to the database
        try:
            for row_tuple in imported_data:
                row_dict = dict(zip(imported_data.headers, row_tuple))
                serializer = StudentSerializers(data=row_dict)
                if serializer.is_valid():
                    serializer.save()
                else:
                    # Handle validation errors
                    error_details = [{'field': field, 'message': message} for field, message in serializer.errors.items()]
                    print("Validation errors:", error_details)
                    return Response({'message': 'Validation error', 'errors': error_details}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Data imported successfully'})
        except Exception as e:
            # Handle other exceptions
            print(f'Error importing data: {str(e)}')
            return Response({'message': f'Error importing data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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