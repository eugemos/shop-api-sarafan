from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
)

from .views import (
    CategoryListView, ProductInCartView, ProductListView, CartView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('products/', ProductListView.as_view()),
    path('cart/<slug:product>/', ProductInCartView.as_view()),
    path('cart/', CartView.as_view()),

    path('auth/', include('djoser.urls.authtoken')),

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
