from django.db import transaction
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from office.serializers import CategorySerializer, BrandSerializer, ArticleSerializer, ProductSerializer, \
    CustomerSerializer, PaymentSerializer, SaleSerializer, ShippingSerializer, SaleItemSerializer, PurchaseSerializer, \
    PurchaseItemSerializer
from products.models import Brand, Category, Article, Product
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


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
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
        queryset = self.queryset.order_by('-created', 'id')
        article = self.request.GET.get('article')
        name = self.request.GET.get('name')

        if article:
            queryset = queryset.filter(article__pk=article)

        if name:
            queryset = queryset.filter(sku=name)

        return queryset


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
        print(self.request.user)
        serializer.save(user=self.request.user)