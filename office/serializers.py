from django.db.models import Sum
from rest_framework import serializers

from products.models import Category, Brand, Article, Product
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


class ArticleSerializer(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()

    def get_brand_name(self, value):
        if value.brand:
            return value.brand.name
        return '-'

    class Meta:
        model = Article
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    article_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    def get_article_name(self, obj):
        if obj.article:
            return obj.article.name
        return ''

    def get_brand_name(self, obj):
        if obj.article:
            if obj.article.brand:
                return obj.article.brand.name
        return ''

    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return ''

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
    product_article = serializers.SerializerMethodField()
    product_sku = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()

    def get_brand(self, value):
        if value.product:
            if value.product.article:
                if value.product.article.brand:
                    return value.product.article.brand.name
        return ''

    def get_product_name(self, value):
        if value.product:
            return value.product.name
        return ''

    def get_product_article(self, value):
        if value.product:
            if value.product.article:
                return value.product.article.name
        return ''

    def get_product_sku(self, value):
        if value.product:
            return value.product.sku
        return ''

    class Meta:
        model = PurchaseItem
        fields = '__all__'

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
    class Meta:
        model = SaleItem
        fields = '__all__'