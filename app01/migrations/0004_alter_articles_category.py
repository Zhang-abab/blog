# Generated by Django 3.2 on 2022-04-21 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_articles_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='category',
            field=models.IntegerField(blank=True, choices=[(1, '前端'), (2, '后端'), (3, '项目相关')], null=True, verbose_name='文章分类'),
        ),
    ]
