# Generated by Django 3.2 on 2022-05-05 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_alter_articles_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='word',
            field=models.IntegerField(default=0, verbose_name='文字字数'),
        ),
    ]
