# Generated by Django 4.1.4 on 2023-01-03 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, default='placeholder.png', null=True, upload_to='<django.db.models.fields.CharField>'),
        ),
    ]
