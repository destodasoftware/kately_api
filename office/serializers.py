from django.contrib.auth.models import User
from django.db.models import Sum, F
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from products.models import Category, Brand, Product
from purchasing.models import Purchase, PurchaseItem
from sales.models import Sale, Payment, Shipping, SaleItem
from users.models import Customer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    root_name = serializers.SerializerMethodField()
    number_variation = serializers.SerializerMethodField()
    total_stock = serializers.SerializerMethodField()

    def get_number_variation(self, obj):
        if obj.product_set.all():
            return obj.product_set.all().count()
        return None

    def get_total_stock(self, obj):
        if obj.product_set.all():
            summary = []
            for variant in obj.product_set.all():
                summary.append(variant.stock)

            return sum(summary)
        return obj.stock

    def get_root_name(self, obj):
        if obj.root:
            return obj.root.name
        return None

    def get_brand_name(self, obj):
        if obj.brand:
            return obj.brand.name
        return ''

    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return ''

    def update(self, instance, validated_data):
        data = super(ProductSerializer, self).update(instance, validated_data)
        if data.product_set.all():
            for variant in data.product_set.all():
                size = variant.size if variant.size else ''
                color = variant.color if variant.color else ''
                variant.name = '{} {} {}'.format(data.name, size, color)
                variant.brand = data.brand
                variant.category = data.category
                variant.save()
        else:
            size = data.size if data.size else ''
            color = data.color if data.color else ''
            if data.root:
                data.name = '{} {} {}'.format(data.root.name, size, color)
            else:
                data.name = '{} {} {}'.format(data.name, size, color)

            data.save()

        return data

    def create(self, validated_data):
        data = super(ProductSerializer, self).create(validated_data)
        if data.product_set.all():
            for variant in data.product_set.all():
                size = variant.size if variant.size else ''
                color = variant.color if variant.color else ''
                variant.name = '{} {} {}'.format(data.name, size, color)
                variant.brand = data.brand
                variant.category = data.category
                variant.save()
        else:
            size = data.size if data.size else ''
            color = data.color if data.color else ''
            if data.root:
                data.name = '{} {} {}'.format(data.root.name, size, color)
            else:
                data.name = '{} {} {}'.format(data.name, size, color)

            data.save()

        return data

    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    pic = serializers.SerializerMethodField()
    total_stock = serializers.SerializerMethodField()

    def get_pic(self, value):
        if value.user:
            return value.user.username
        return '-'

    def get_total_stock(self, value):
        if value.purchaseitem_set.all():
            return value.purchaseitem_set.all().aggregate(Sum('quantity')).get('quantity__sum', 0)
        return 0

    class Meta:
        model = Purchase
        fields = '__all__'


class PurchaseItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_sku = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()

    def get_brand(self, value):
        if value.product:
            if value.product:
                if value.product.brand:
                    return value.product.brand.name
        return ''

    def get_product_name(self, value):
        if value.product:
            return value.product.name
        return ''

    def get_product_sku(self, value):
        if value.product:
            return value.product.sku
        return ''

    class Meta:
        model = PurchaseItem
        fields = '__all__'

    def validate_purchase(self, value):
        if value.is_adjusment:
            raise serializers.ValidationError('This purchase has been adjustment! ')
        return value

    def create(self, validated_data):
        product = validated_data.get('product')
        purchase = validated_data.get('purchase')
        p, created = PurchaseItem.objects.get_or_create(product=product, purchase=purchase)

        if created:
            p.quantity = validated_data.get('quantity')
        else:
            p.quantity = p.quantity + 1

        p.save()
        return p


class SaleSerializer(serializers.ModelSerializer):
    pic = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    shipping = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_shipping(self, value):
        try:
            return value.shipping.pk
        except:
            return None

    def get_total(self, value):
        if value.saleitem_set.all():
            sale_items = value.saleitem_set.all()
            return sale_items.aggregate(total=Sum(F('price') * F('quantity'))).get('total')
        return 0

    def get_brand_name(self, value):
        if value.brand:
            return value.brand.name
        return '-'

    def get_pic(self, value):
        if value.user:
            return value.user.username
        return '-'

    class Meta:
        model = Sale
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_stock = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.quantity * obj.price

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_stock(self, obj):
        if obj.product.stock:
            return obj.product.stock
        return 0

    def update(self, instance, validated_data):
        current_quantity = instance.quantity
        change_quantity = validated_data.get('quantity')
        stock = instance.product.stock

        if (stock + current_quantity) - change_quantity < 0:
            raise serializers.ValidationError('Stock not available')

        data = super(SaleItemSerializer, self).update(instance, validated_data)
        data.product.stock = (stock + current_quantity) - change_quantity
        data.product.save()
        return data

    def create(self, validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        if product.stock - quantity < 0:
            raise serializers.ValidationError('Stock not available')

        data = super(SaleItemSerializer, self).create(validated_data)

        # Reduce stock product
        product.stock = product.stock - quantity
        product.save()

        return data

    class Meta:
        model = SaleItem
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=SaleItem.objects.all(),
                fields=['product', 'sale']
            )
        ]


class ReportSaleItemSerializer(serializers.ModelSerializer):
    product_code = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_root = serializers.SerializerMethodField()
    sale_number = serializers.SerializerMethodField()
    current_stock = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_product_code(self, obj):
        return obj.product.sku

    def get_current_stock(self, obj):
        return obj.product.stock

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_root(self, obj):
        if obj.product.root:
            return obj.product.root.name

    def get_sale_number(self, obj):
        if obj.sale:
            return obj.sale.sale_number
        return ''

    def get_total(self, obj):
        return obj.quantity * obj.price

    class Meta:
        model = SaleItem
        fields = '__all__'



