# Generated by Django 2.2.4 on 2022-06-28 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogs',
            name='user_saved',
        ),
        migrations.AlterField(
            model_name='blogs',
            name='content',
            field=models.TextField(),
        ),
    ]