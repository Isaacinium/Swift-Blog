# Generated by Django 5.0.7 on 2024-12-07 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='dp.png', upload_to='post_pics'),
        ),
    ]
