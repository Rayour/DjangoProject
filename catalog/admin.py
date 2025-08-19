from django.contrib import admin

from catalog.models import Category, Contact, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "country", "tin", "address")
    list_filter = ("country",)
    search_fields = ("tin",)
