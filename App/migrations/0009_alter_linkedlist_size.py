# Generated by Django 4.2 on 2023-12-24 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_linkedlist_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkedlist',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
