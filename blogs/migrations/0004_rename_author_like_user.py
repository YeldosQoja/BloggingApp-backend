# Generated by Django 5.0.3 on 2024-05-05 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_remove_blog_likes_remove_comment_likes_like_blog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='author',
            new_name='user',
        ),
    ]
