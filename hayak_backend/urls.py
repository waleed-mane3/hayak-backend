from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from account.api.views import get_health

# Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Hayak APIs",
      default_version='v1',
      description="API Documentation for Hayak",
      terms_of_service="",
      contact=openapi.Contact(email="info@hayaksa.com"),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_system.api.urls')),
    path('api/account/', include('account.api.urls')),
    path('api/event/', include('event.api.urls')),
    path('api/webhooks/', include('webhook.urls')),
    path('api/package/', include('package.api.urls')),
    path('api/scan/', include('scan.api.urls')),
    path('api/design/', include('design.api.urls')),
    path('api/health/', get_health),
    path('api/billing/', include('billing.api.urls')),

    # Swagger
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)