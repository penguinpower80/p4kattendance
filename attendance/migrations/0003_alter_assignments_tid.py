# Generated by Django 4.0.3 on 2022-03-12 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_assignments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='tid',
            field=models.CharField(max_length=50),
        ),
    ]
