# Generated by Django 2.0.6 on 2018-07-18 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0023_bookmarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmarks',
            name='o_id',
            field=models.IntegerField(unique=True),
        ),
    ]
