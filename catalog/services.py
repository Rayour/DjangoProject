from django.core.cache import cache

from config.settings import CACHE_ENABLED, CACHE_TIME

from .models import Category, Product


class ProductService:
    """Класс для реализации бизнес логики модели продуктов"""

    @staticmethod
    def get_product_page_queryset(page, per_page, category_id):
        """Метод получения списка товаров для страницы"""

        start = page * per_page - per_page
        stop = start + per_page

        if CACHE_ENABLED:
            products = cache.get(f"product_page_{page}_{per_page}_{category_id}")
            if products:
                return products
            else:
                if category_id:
                    products = Product.objects.filter(is_published=True, category_id=category_id).order_by(
                        "created_at")[start:stop]
                else:
                    products = Product.objects.filter(is_published=True).order_by("created_at")[start:stop]
                cache.set(products, f"product_page_{page}_{per_page}_{category_id}", CACHE_TIME)
                return products
        else:
            if category_id:
                products = Product.objects.filter(is_published=True, category_id=category_id).order_by("created_at")[
                           start:stop]
            else:
                products = Product.objects.filter(is_published=True).order_by("created_at")[
                           start:stop]
            return products

    @staticmethod
    def get_page_count(per_page, category_id):
        """Метод получения количества страниц отображения товаров"""

        if category_id:
            products_count = Product.objects.filter(is_published=True, category_id=category_id).count()
        else:
            products_count = Product.objects.filter(is_published=True).count()

        if products_count % per_page:
            page_count = products_count // per_page + 1
        else:
            page_count = products_count // per_page

        return page_count

    @staticmethod
    def get_pages(page_count):
        """Метод получения списка страниц отображения товаров"""

        pages = [i + 1 for i in range(page_count)]
        return pages

    @staticmethod
    def get_prev_next_page(page, page_count):
        """Метод получения предыдущей и следующей страницы списка товаров"""

        if 1 < page < page_count:
            prev_page = page - 1
            next_page = page + 1
        elif page <= 1:
            page = 1
            prev_page = 1
            next_page = page + 1
        else:
            page = page_count
            prev_page = page - 1
            next_page = page_count

        return page, prev_page, next_page


class CategoryService:
    """Класс для реализации бизнес логики модели категорий"""

    @staticmethod
    def get_categories_list():
        """Метод получения всех категорий товаров"""

        if CACHE_ENABLED:
            categories = cache.get("category_list")
            if categories:
                return categories
            else:
                categories = Category.objects.all()
                cache.set(categories, "category_list", CACHE_TIME)
                return categories
        else:
            categories = Category.objects.all()
            return categories

    @staticmethod
    def is_category_exist(category_id):
        """Метод определения существования категории"""

        if Category.objects.get(id=category_id):
            return True
        return False
