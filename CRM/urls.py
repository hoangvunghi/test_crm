from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView,SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('api/', include('product.urls')),
    path('api/', include('taskboard.urls')),
    path('api/', include('customer.urls')),
    path("api/", include("employee.urls")),
    
    path("api/schema/",SpectacularAPIView.as_view(),name="schema"),
    path("docs/",SpectacularSwaggerView.as_view(url_name="schema")),
    path("redoc/",SpectacularRedocView.as_view(url_name="schema")),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]