# Generated by Django 4.2 on 2023-04-29 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_birth',
            field=models.DateField(blank=True),
        ),
    ]