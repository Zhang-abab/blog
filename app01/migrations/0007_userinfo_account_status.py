# Generated by Django 3.2 on 2022-05-08 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_auto_20220508_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='account_status',
            field=models.IntegerField(choices=[(0, '账号正常'), (1, '账号异常'), (2, '账号被封禁')], default=0, verbose_name='账号状态'),
        ),
    ]
