# Generated by Django 5.1.2 on 2024-10-25 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_member_bookcopy_bookrent'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='library.author'),
        ),
    ]
