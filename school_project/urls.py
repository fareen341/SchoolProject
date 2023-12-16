"""school_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from enroll import views
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register('student', views.StudentViewSet, basename='student')
router.register('parent', views.ParentViewSet, basename='parent')
router.register('document_upload', views.DocumentUploadViewSet, basename='document_upload')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('enroll/', views.Enroll.as_view(), name='enroll'),
    path('enroll/success/', views.SuccessView.as_view(), name='success'),
    path('student/import-export/', views.StudentImportExportView.as_view(), name='student_import_export'),
]

if settings.DEBUG:		# for developer mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

