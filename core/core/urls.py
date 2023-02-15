from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse


def startup(request):
    return HttpResponse("<h1>s.nasiri.cs@gmail.com</h1>", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', startup),
    path('blog/', include('blog.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

