from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe
from rest_framework.filters import SearchFilter

from recipes.models import Tag


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilters(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.order_by('-tags'),
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

    def filter_author(self, queryset, name, value):
        if value:
            return queryset.filter(author=value)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(carts=self.request.user.id)
        return queryset
