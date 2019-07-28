from django.urls import path
from rest_framework.routers import DefaultRouter

from office.views import OfficeAuthToken, CategoryViewSet, BrandViewSet, ArticleViewSet

urlpatterns = [
    path('api-token-auth/', OfficeAuthToken.as_view()),
]

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'articles', ArticleViewSet, basename='article')
urlpatterns += router.urls
