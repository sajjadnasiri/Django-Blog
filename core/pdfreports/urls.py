from django.urls import path
from .views import pdf_create_view

appname = "pdf"

urlpatterns = [
    path("", pdf_create_view, name="pdf-create")
]