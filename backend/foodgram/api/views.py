from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED)
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import IngredientFilter
from .paginators import LimitPageNumberPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (IngredientSerializer,
                          TagSerializer, UserSerializer,
                          SubscribeSerializer)
from recipes.models import Ingredient, Tag

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all().order_by('-first_name')
    serializer_class = UserSerializer
    additional_serializer = SubscribeSerializer
    pagination_class = LimitPageNumberPagination

    @action(methods=('POST', 'DELETE'), detail=True)
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

    @action(methods=('GET',), detail=False)
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
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
