from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=64,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=64,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тэг',
        max_length=64,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=7,
        blank=True,
        null=True,
        default='#',
        unique=True,
        validators=[
            RegexValidator(
                "^#([A-Fa-f0-9]{6})$",
                "введите код цвета в формате #F08080"
            ),
        ],
    )
    slug = models.CharField(
        verbose_name='Слаг тэга',
        max_length=32,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} (цвет: {self.color})'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тэги'
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipes/',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[MinValueValidator]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.name}. Автор: {self.author.username}'


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        verbose_name='В рецептах',
        related_name='ingredient_amount',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        verbose_name='Связанные ингредиенты',
        related_name='ingredient_amount',
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
        validators=(
            MinValueValidator(
                1, 'Минимальное значение 1'
            ),
            RegexValidator(
                '^[0-9]+$',
                (
                    'Количество ингредиента может быть '
                    'только числом >=1'
                )
            ),
        ),
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('recipe', )

    def __str__(self):
        return f'{self.ingredients}'


class FavoriteShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user} :: {self.recipe}'


class Favorite(FavoriteShoppingCart):

    class Meta(FavoriteShoppingCart.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(FavoriteShoppingCart):

    class Meta(FavoriteShoppingCart.Meta):
        default_related_name = 'shopping_list'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
