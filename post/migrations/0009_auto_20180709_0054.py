# Generated by Django 2.0.6 on 2018-07-08 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_auto_20180707_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='head_img',
            field=models.ImageField(null=True, upload_to='', verbose_name='Title Image'),
        ),
    ]
