# Generated by Django 3.1.14 on 2023-05-29 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20230525_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='article/%Y%m%d/'),
        ),
    ]
