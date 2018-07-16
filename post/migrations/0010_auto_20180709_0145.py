# Generated by Django 2.0.6 on 2018-07-08 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20180709_0054'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLikers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users_id', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='downvoter',
            name='post',
        ),
        migrations.RemoveField(
            model_name='upvoter',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='downvote',
        ),
        migrations.DeleteModel(
            name='Downvoter',
        ),
        migrations.DeleteModel(
            name='Upvoter',
        ),
        migrations.AddField(
            model_name='postlikers',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
    ]
