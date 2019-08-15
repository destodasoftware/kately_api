from django.urls import path
from rest_framework.routers import DefaultRouter

from office.views import OfficeAuthToken, CategoryViewSet, BrandViewSet, ProductViewSet, \
    PurchaseItemViewSet, PurchaseViewSet, SaleViewSet, CustomerViewSet, ShippingViewSet, SaleItemViewSet, \
    ReportSaleItemViewSet, PaymentViewSet, SaleReportViewSet

urlpatterns = [
    path('api-token-auth/', OfficeAuthToken.as_view()),
]

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'purchases', PurchaseViewSet, basename='purchase')
router.register(r'purchaseitems', PurchaseItemViewSet, basename='purchaseitem')
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'salereports', SaleReportViewSet, basename='salereport')
router.register(r'saleitems', SaleItemViewSet, basename='saleitem')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'shippings', ShippingViewSet, basename='shipping')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'reportsaleitems', ReportSaleItemViewSet, basename='reportsaleitems')
urlpatterns += router.urls
