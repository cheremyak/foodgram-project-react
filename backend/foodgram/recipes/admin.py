from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Cart, Favorite, Ingredient,
                     IngredientAmount, Recipe, Tag)


class IngredientInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'get_image',
                    'get_favorites',)
    readonly_fields: ('get_image',)
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )
    raw_id_fields = ('author', )
    search_fields = (
        'name', 'author__username', 'author__email'
    )
    list_filter = (
        'name', 'author__username', 'tags__name',
    )
    save_on_top = True
    inlines = (IngredientInline,)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30">')
    get_image.short_description = 'Изображение'

    def get_favorites(self, obj):
        return obj.favorite.count()
    get_favorites.short_description = 'В избранном'


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    list_filter = ('user',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
