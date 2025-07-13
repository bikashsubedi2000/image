# digitelhelp/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Import the new homepage view
from backgroundremover.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),

    # The new homepage URL
    path('', homepage, name='homepage'),

    # URLs for each specific tool
    path('remove-bg/', include('backgroundremover.urls')),
    path('resize/', include('imageresizer.urls')),
    path('convert/', include('imageconverter.urls')),
]

# This part remains the same
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)