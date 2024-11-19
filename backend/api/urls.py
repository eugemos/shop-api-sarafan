from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
)

from .views import CategoryListView, ProductListView


urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('products/', ProductListView.as_view()),

    path('auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
