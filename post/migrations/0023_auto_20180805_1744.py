# Generated by Django 2.0.6 on 2018-08-05 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0022_auto_20180805_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_topic',
            field=models.CharField(choices=[('0', 'PERSONAL'), ('1', 'FUTURE'), ('2', 'CULTURE'), ('3', 'TECH'), ('4', 'ENTREPRENEURSHIP'), ('5', 'SELF'), ('6', 'POLITICS'), ('7', 'DESIGN'), ('8', 'SCIENCE'), ('9', 'POPULAR')], default=0, max_length=1),
        ),
    ]
