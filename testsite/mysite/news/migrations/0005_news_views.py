# Generated by Django 3.2.7 on 2021-09-11 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_news_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='views',
            field=models.ImageField(default=0, upload_to=''),
        ),
    ]
