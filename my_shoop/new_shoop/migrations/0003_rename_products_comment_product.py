# Generated by Django 5.0.6 on 2024-07-28 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_shoop', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='products',
            new_name='product',
        ),
    ]
