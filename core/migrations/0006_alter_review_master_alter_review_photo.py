# Generated by Django 5.2 on 2025-06-14 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_master_view_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.master', verbose_name='Мастер'),
        ),
        migrations.AlterField(
            model_name='review',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/reviews/', verbose_name='Фотография'),
        ),
    ]
