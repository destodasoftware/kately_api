from products.models import Product


class ProductCore:
    @staticmethod
    def calculate_updating_childs(obj):
        if obj.product_set.all():
            for variant in obj.product_set.all():
                variant.brand = obj.brand
                variant.category = obj.category
                variant.name = f'{obj.name} {variant.size} {variant.color}'
                variant.save()

    @staticmethod
    def calculation_stock_parent(obj):
        # If product variant
        if obj.root:
            product = obj.root
            variants = Product.objects.filter(root=product)
            total = []
            for variant in variants:
                total.append(variant.stock)

            product.stock = sum(total)
            product.save()

        else:
            variants = Product.objects.filter(root=obj)
            if variants:
                total = []
                for variant in variants:
                    total.append(variant.stock)

                obj.stock = sum(total)
                obj.save()

    @staticmethod
    def calculation_stock_redused(obj):
        # If product variant
        if obj.root is None:
            product = obj.root
            variants = Product.objects.filter(root=product)
            total = []
            for variant in variants:
                total.append(variant.stock)

            product.stock = sum(total)
            product.save()




