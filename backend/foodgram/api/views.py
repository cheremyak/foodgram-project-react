from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import (Cart, Favorite, Ingredient,
                            IngredientAmount, Recipe, Tag)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilters
from .paginators import LimitPageNumberPagination
from .permissions import IsAdminOrReadOnly, UserAndAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          SubscribeSerializer,
                          TagSerializer, UserSerializer)


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = LimitPageNumberPagination
    additional_serializer = SubscribeSerializer

    @action(
        detail=True,
        methods=('POST', 'DELETE',),
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        obj = get_object_or_404(self.queryset, id=kwargs.get('id'))
        serializer = self.additional_serializer(
            obj, context={'request': self.request}
        )
        if self.request.method == 'POST':
            user.subscribe.add(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            user.subscribe.remove(obj)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=('GET',),
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        authors = user.subscribe.all()
        pages = self.paginate_queryset(authors)
        serializer = SubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.order_by('-name')
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.order_by('name')
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    filter_backends = [IngredientFilter]


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeCreateSerializer
    permission_classes = (UserAndAdminOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    filter_class = RecipeFilters

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def add_to_list(model, user, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @staticmethod
    def delete_from_list(model, user, pk):
        instance = model.objects.filter(user=user, recipe__id=pk)
        if not instance.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to_list(Favorite, request.user, pk)
        return self.delete_from_list(Favorite, request.user, pk)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to_list(Cart, request.user, pk)
        return self.delete_from_list(Cart, request.user, pk)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientAmount.objects
            .filter(recipe__carts__user=request.user)
            .values('ingredients__name', 'ingredients__measurement_unit')
            .annotate(amount=Sum('amount'))
        )
        shopping_cart = [f'Список покупок для пользователя {request.user}.\n']
        for ingredient in ingredients:
            shopping_cart.append(
                f'{ingredient["ingredients__name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["ingredients__measurement_unit"]}\n'
            )
        file = f'{request.user}_shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={file}'
        return response
