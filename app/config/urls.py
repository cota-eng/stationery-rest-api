from django.conf import settings
from django.conf.urls.static import static
import environ
from django.contrib import admin
from django.urls import path, include

import os
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))
ADMIN_URL = env('ADMIN_URL')

urlpatterns = [
    path('api/', include("blog.urls")),
    path('api/', include("authentication.urls")),
    path('api/', include("pen.urls")),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
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
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('dj/', include("dj_rest_auth.urls")),
        path('', schema_view.with_ui('swagger', cache_timeout=0),
             name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc',
             cache_timeout=0), name='schema-redoc'),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
