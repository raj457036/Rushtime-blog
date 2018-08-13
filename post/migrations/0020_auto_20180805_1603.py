# Generated by Django 2.0.6 on 2018-08-05 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0019_remove_reply_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_topic',
        ),
        migrations.AddField(
            model_name='post',
            name='post_tags',
            field=models.CharField(default='everyday', max_length=255),
            preserve_default=False,
        ),
    ]
