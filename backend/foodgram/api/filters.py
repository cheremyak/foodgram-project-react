from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient


class IngredientFilter(FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)
