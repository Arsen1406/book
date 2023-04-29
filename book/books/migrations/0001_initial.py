# Generated by Django 4.2 on 2023-04-29 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1024)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
