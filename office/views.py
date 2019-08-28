import csv
import datetime

from django.db import transaction
from django.db.models import Sum, F, Max, Avg, Count
from django.http import HttpResponse

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import NotAcceptable, NotFound, ValidationError
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from cores.core import ProductCore
from cores.mails import send_email_order
from office.serializers import CategorySerializer, BrandSerializer, ProductSerializer, \
    CustomerSerializer, PaymentSerializer, SaleSerializer, ShippingSerializer, SaleItemSerializer, PurchaseSerializer, \
    PurchaseItemSerializer, ReportSaleItemSerializer, SaleReportSerializer
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
    queryset = Customer.objects.all().order_by('-created')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.GET.get('name')
        customer_number = self.request.GET.get('customer_number')

        if name:
            queryset = queryset.filter(name__icontains=name)

        if customer_number:
            queryset = queryset.filter(customer_number=customer_number)

        return queryset

    @action(detail=False)
    def export(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        filename = f"CUSTOMER-{datetime.datetime.now().strftime('%Y-%m-%d %H:%I:%S')}.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        queryset = self.get_queryset()
        data = self.serializer_class(queryset, many=True)
        header_fields = [
            'Kode Pelanggan',
            'Nama Pelanggan',
            'Email Pelanggan',
            'Regional',
            'Kota',
            'Order',
            'Penjualan',
        ]

        writer = csv.writer(response)
        writer.writerow(header_fields)
        for obj in data.data:
            writer.writerow([
                obj.get('customer_number'),
                obj.get('name'),
                obj.get('email'),
                obj.get('country'),
                obj.get('city'),
                obj.get('total_orders'),
                obj.get('total_sales')
            ])

        return response

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-created')
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
        brand = self.request.GET.get('brand')
        sku = self.request.GET.get('sku')

        if brand:
            queryset = queryset.filter(brand__pk=brand)

        if show_root:
            queryset = queryset.filter(root=None)

        if article:
            queryset = queryset.filter(article__pk=article)

        if name:
            queryset = queryset.filter(name__icontains=name)

        if sku:
            queryset = queryset.filter(sku=sku)

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
        sale_number = self.request.GET.get('sale_number')
        name = self.request.GET.get('name')
        sale = self.request.GET.get('sale')

        if sale_number:
            queryset = queryset.filter(sale__sale_number=sale_number)

        if sale:
            queryset = queryset.filter(sale__pk=sale)

        if name:
            qs = queryset.filter(product__sku=name)
            if not qs:
                queryset = queryset.filter(product__name__icontains=name)
            else:
                queryset = qs

        return queryset

    @action(detail=False)
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'nomer_order',
            'brand',
            'customer_name',
            'customer_phone',
            'customer_email',
            'shipping_address',
            'shipping_cost',
            'tracking_number',
            'courier',
            'product_name',
            'size',
            'color',
            'quantity',
            'price',
            'discount',
            'line_total',
        ])
        queryset = self.get_queryset()
        for data in queryset:
            if data.sale:
                brand = ''
                customer_name = ''
                customer_phone = ''
                customer_email = ''
                shipping_address = ''
                shipping_cost = ''
                tracking_number = ''
                courier = ''
                discount = ''

                if data.sale.brand:
                    brand = data.sale.brand.name

                if data.sale.customer:
                    customer_name = data.sale.customer.name
                    customer_email = data.sale.customer.email
                    customer_phone = data.sale.customer.phone

                if Shipping.objects.filter(sale=data.sale):
                    shipping = Shipping.objects.get(sale=data.sale)
                    shipping_address = f'{shipping.address} ' \
                                       f'{shipping.province}, ' \
                                       f'{shipping.city}, ' \
                                       f'{shipping.country}, {shipping.postal_code}'
                    tracking_number = shipping.tracking_number
                    shipping_cost = shipping.cost
                    courier = shipping.courier_service

                if data.is_percent:
                    discount = f'{data.discount}%'
                else:
                    discount = f'Rp.{data.discount}'

                writer.writerow([
                    data.sale.sale_number,
                    brand,
                    customer_name,
                    customer_phone,
                    customer_email,
                    shipping_address,
                    shipping_cost,
                    tracking_number,
                    courier,
                    data.product.name,
                    data.product.size,
                    data.product.color,
                    data.quantity,
                    data.price,
                    discount,
                    data.total()
                ])

        return response

    @action(detail=False)
    def export_pakde(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'order_number',
            'client_name',
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_address',
            'product_name',
            'size_name',
            'courier',
            'no_resi',
            'quantity',
            'ongkir'
        ])
        queryset = self.get_queryset()
        for data in queryset:
            if data.sale:
                brand = ''
                customer_name = ''
                customer_phone = ''
                customer_email = ''
                shipping_address = ''
                shipping_cost = ''
                tracking_number = ''
                courier = ''
                discount = ''

                if data.sale.brand:
                    brand = data.sale.brand.name

                if data.sale.customer:
                    customer_name = data.sale.customer.name
                    customer_email = data.sale.customer.email
                    customer_phone = data.sale.customer.phone

                if Shipping.objects.filter(sale=data.sale):
                    shipping = Shipping.objects.get(sale=data.sale)
                    shipping_address = f'{shipping.address} ' \
                                       f'{shipping.province}, ' \
                                       f'{shipping.city}, ' \
                                       f'{shipping.country}, {shipping.postal_code}'
                    tracking_number = shipping.tracking_number
                    shipping_cost = shipping.cost
                    courier = shipping.courier_service

                if data.is_percent:
                    discount = f'{data.discount}%'
                else:
                    discount = f'Rp.{data.discount}'

                writer.writerow([
                    data.sale.sale_number,
                    brand,
                    customer_name,
                    customer_email,
                    customer_phone,
                    shipping_address,
                    data.product.name,
                    data.product.size,
                    courier,
                    tracking_number,
                    shipping_cost
                ])

        return response

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

    def get_queryset(self):
        queryset = self.queryset
        purchase_number = self.request.GET.get('purchase_number')
        brand = self.request.GET.get('brand')

        if purchase_number:
            queryset = queryset.filter(purchase_number=purchase_number)

        if brand:
            queryset = queryset.filter(brand__pk=brand)

        return queryset

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
        brand = self.request.GET.get('brand')
        temps = queryset

        if sale_number:
            queryset = queryset.filter(sale_number=sale_number)

        if brand:
            queryset = queryset.filter(brand__pk=brand)

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

    @action(detail=False, methods=['get'])
    def report(self, request):
        queryset = self.queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SaleReportSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SaleReportSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_mail(self, request, pk=None):
        sale = self.get_object()
        send_email_order(sale, sale.user.email, sale.customer.email)
        return Response({'ok': True})

    @action(detail=False)
    def chart(self, request):

        sales = Payment.objects.filter(is_paid=True).values('sale__brand__name').annotate(
            Sum('amount')
        )
        categories = []
        series = []
        for sale in sales:
            series.append({
                'name': sale.get('sale__brand__name'),
                'data': sale.get('amount__sum')
            })

        result = {
            'categories': categories,
            'series': series
        }

        return Response(result)


class ShippingViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingSerializer
    queryset = Shipping.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class SaleReportViewSet(viewsets.ModelViewSet):
    serializer_class = SaleReportSerializer
    queryset = Sale.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        brand = self.request.GET.get('brand')
        is_paid = self.request.GET.get('is_paid')

        if is_paid == 'true':
            val_list = Payment.objects.filter(is_paid=True).values_list('sale')
            queryset = queryset.filter(pk__in=val_list)

        if brand:
            queryset = queryset.filter(brand__pk=brand)

        if start_date and end_date:
            start_date = [int(i) for i in start_date.split('-')]
            end_date = [int(i) for i in end_date.split('-')]

            queryset = queryset.filter(
                create__gte=datetime.date(*start_date),
                create__lte=datetime.date(*end_date)
            )

        return queryset

    @action(detail=False)
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Tanggal',
            'Nomer Penjualan',
            'Nama Produk',
            'Harga',
            'Jumlah',
            'Diskon',
            'Jenis Diskon',
            'Subtotal'
        ])
        queryset = self.get_queryset()
        for data in queryset:
            for i in data.saleitem_set.all():
                writer.writerow([
                    data.create,
                    i.sale.sale_number,
                    i.product.name,
                    i.price,
                    i.quantity,
                    i.discount,
                    i.is_percent,
                    i.total()
                ])

        return response


class ReportSaleItemViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSaleItemSerializer
    queryset = SaleItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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

