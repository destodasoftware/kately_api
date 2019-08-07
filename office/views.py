from django.db import transaction
from django.db.models import Sum, F, Max, Avg, Count
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from cores.core import ProductCore
from office.serializers import CategorySerializer, BrandSerializer, ProductSerializer, \
    CustomerSerializer, PaymentSerializer, SaleSerializer, ShippingSerializer, SaleItemSerializer, PurchaseSerializer, \
    PurchaseItemSerializer, ReportSaleItemSerializer
from products.models import Brand, Category, Product
from purchasing.models import PurchaseItem, Purchase
from sales.models import Sale, Payment, Shipping, SaleItem
from users.models import Customer


class OfficeAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter().order_by('-created', 'id')
        article = self.request.GET.get('article')
        name = self.request.GET.get('name')
        root = self.request.GET.get('root')
        show_root = self.request.GET.get('show_root')

        if show_root:
            queryset = queryset.filter(root=None)

        if article:
            queryset = queryset.filter(article__pk=article)

        if name:
            temp = queryset.filter(sku=name)

            if not temp:
                queryset = queryset.filter(name__icontains=name)

        if root:
            queryset = queryset.filter(root__pk=root)

        return queryset


class SaleItemViewSet(viewsets.ModelViewSet):
    serializer_class = SaleItemSerializer
    queryset = SaleItem.objects.all().order_by('-created', 'id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter().order_by('-created', 'id')
        sale = self.request.GET.get('sale')
        name = self.request.GET.get('name')

        if sale:
            queryset = queryset.filter(sale__pk=sale)

        if name:
            qs = queryset.filter(product__sku=name)
            if not qs:
                queryset = queryset.filter(product__name__icontains=name)
            else:
                queryset = qs

        return queryset

    def perform_destroy(self, instance):
        # Re stock again
        stock = instance.quantity
        instance.product.stock = instance.product.stock + stock
        instance.product.save()
        instance.delete()


class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all().order_by('-created', 'id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['put'])
    def adjustment(self, request, pk=None):
        try:
            with transaction.atomic():
                purchase = self.get_object()
                if purchase.is_adjusment is False and purchase.purchaseitem_set.all():
                    for pi in purchase.purchaseitem_set.all():
                        pi.product.stock = pi.product.stock + pi.quantity
                        pi.product.save()

                    purchase.is_adjusment = True
                    purchase.save()
            return Response(self.serializer_class(purchase, many=False).data)
        except:
            raise NotAcceptable('Adjustment not accepted')

    def perform_destroy(self, instance):
        if instance.is_adjusment is False:
            instance.delete()


class PurchaseItemViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseItemSerializer
    queryset = PurchaseItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.order_by('-created', 'id')
        purchase = self.request.GET.get('purchase')

        if purchase:
            queryset = queryset.filter(purchase__pk=purchase)

        return queryset

    def perform_destroy(self, instance):
        if instance.purchase.is_adjusment is False:
            instance.delete()


class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.order_by('-created', 'id')
        sale_number = self.request.GET.get('sale_number')

        if sale_number:
            queryset = queryset.filter(sale_number=sale_number)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # Restock all product
        if instance.saleitem_set.all():
            sale_items = instance.saleitem_set.all()
            for sale_item in sale_items:
                product = sale_item.product
                product.stock = product.stock + sale_item.quantity
                product.save()

        instance.delete()

class ShippingViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingSerializer
    queryset = Shipping.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ReportSaleItemViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSaleItemSerializer
    queryset = SaleItem.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(quantity__gt=0, price__gt=0)

        return queryset

    @action(detail=False)
    def summary(self, request):
        queryset = self.queryset.filter(quantity__gt=0, price__gt=0)
        summary = queryset.aggregate(
            gross=Sum(F('quantity') * F('price')),
            net=Sum(F('quantity') * (F('price') - F('product__cost'))),
            total_quantity=Sum('quantity'),
            total_customer=Count('sale__customer', distinct=True),
            total_product=Count('product', distinct=True),
            price_average=Avg('price')
        )
        return Response(summary)

