# Generated by Django 3.2.18 on 2023-05-06 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20230506_1359'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ingredientamount',
            name='\nrecipes_ingredientamount Ингредиент уже добавлен\n',
        ),
        migrations.AddConstraint(
            model_name='ingredientamount',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredients'), name='\nrecipes_ingredientamount Ингредиент уже добавлен\n'),
        ),
    ]