# Generated by Django 3.2 on 2022-05-13 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0012_auto_20220512_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='navs',
            field=models.ManyToManyField(blank=True, to='app01.Navs', verbose_name='收藏的网站'),
        ),
    ]
