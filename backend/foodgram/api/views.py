from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import Favorite, Ingredient, IngredientAmount, Recipe, Tag
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilters
from .paginators import LimitPageNumberPagination
from .permissions import IsAdminOrReadOnly, UserAndAdminOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          SubscribeSerializer,
                          TagSerializer, UserSerializer, ShortRecipeSerializer)

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
    additional_serializer = ShortRecipeSerializer
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

    @action(
        detail=True, methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'DELETE':
            if not Favorite.objects.filter(user=user).exists():
                return Response(
                    'Рецепт отсутсвует.',
                    status=HTTP_400_BAD_REQUEST
                )
            Favorite.objects.get(
                user=user,
                recipe=recipe,
            ).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        favorite = Favorite.objects.create(
            user=user,
            recipe=recipe,
        )
        serializer = FavoriteSerializer(
            favorite, context={"request": request}
        )
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(
        methods=('POST', 'DELETE'),
        detail=True
    )
    def shopping_cart(self, request, **kwargs):
        return self._post_delete_obj(request, 'carts', **kwargs)

    @action(
        methods=('GET',),
        detail=False
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.carts.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        ingredients = IngredientAmount.objects.filter(
            recipe__in=(user.carts.values('id'))
        ).values(
            ingredient=F('ingredients__name'),
            measure_unit=F('ingredients__measurement_unit')
        ).annotate(amount_cart=Sum('amount'))
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = ("Список покупок\n")

        for ingr in ingredients:
            shopping_list += (
                f'{ingr["ingredient"]}: '
                f'{ingr["amount_cart"]} '
                f'{ingr["measure_unit"]}\n'
            )
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = (
            f'attachment; filename={filename}.txt'
        )
        return response
