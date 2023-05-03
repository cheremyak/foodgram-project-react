from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        method='filter_tags'
    )
    author = filters.AllValuesFilter(
        method='filter_author'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_tags(self, queryset, name, value):
        if value:
            return queryset.filter(
                tags__slug__in=value).distinct()
        return queryset

    def filter_author(self, queryset, name, value):
        if value:
            return queryset.filter(author=value)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite=self.request.user.id)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(cart=self.request.user.id)
        return queryset
