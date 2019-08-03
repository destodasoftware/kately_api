from django.urls import path
from rest_framework.routers import DefaultRouter

from office.views import OfficeAuthToken, CategoryViewSet, BrandViewSet, ArticleViewSet, ProductViewSet, \
    PurchaseItemViewSet, PurchaseViewSet, SaleViewSet, CustomerViewSet, ShippingViewSet

urlpatterns = [
    path('api-token-auth/', OfficeAuthToken.as_view()),
]

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'purchases', PurchaseViewSet, basename='purchase')
router.register(r'purchaseitems', PurchaseItemViewSet, basename='purchaseitem')
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'shippings', ShippingViewSet, basename='shipping')
urlpatterns += router.urls
