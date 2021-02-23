from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path,include

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import environ
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))
ADMIN_URL = env('ADMIN_URL')

urlpatterns = [
    path('api/', include("authentication.urls")),
    # path('oauth/', include("social_auth.urls")),
    path('api/', include("pen.urls")),
    # path('rest-auth/', include("rest_framework.urls")),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('admin/', admin.site.urls),
    urlpatterns += path('dj/', include("dj_rest_auth.urls")),
else:
    path(ADMIN_URL + '/', admin.site.urls),


# import debug_toolbar
# if settings.DEBUG:
#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] 