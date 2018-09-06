# Generated by Django 2.0.6 on 2018-09-06 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20180904_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=25, verbose_name='年龄'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='points',
            field=models.CharField(default='', max_length=100, verbose_name='教学特点'),
        ),
    ]
