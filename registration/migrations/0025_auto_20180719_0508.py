# Generated by Django 2.0.6 on 2018-07-18 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0024_auto_20180719_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmarks',
            name='bookmark_type',
            field=models.CharField(choices=[('1', 'Post'), ('2', 'Images')], default='1', max_length=1),
        ),
    ]
