# Generated by Django 5.0 on 2024-01-05 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('date_published', models.DateTimeField(verbose_name='date published')),
                ('content', models.TextField(verbose_name='content')),
            ],
        ),
    ]