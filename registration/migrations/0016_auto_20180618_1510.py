# Generated by Django 2.0.6 on 2018-06-18 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0015_userextend_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='img_type',
            field=models.CharField(choices=[('0', 'Profile Pic'), ('1', 'Post Pic'), ('2', 'Article Pic'), ('3', 'Banner Pic')], default='1', max_length=1),
        ),
    ]
