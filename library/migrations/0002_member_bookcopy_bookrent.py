# Generated by Django 5.1.2 on 2024-10-24 16:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email_id', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='BookCopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
            ],
        ),
        migrations.CreateModel(
            name='BookRent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('due_date', models.DateField()),
                ('bookcopy_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.bookcopy')),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.member')),
            ],
        ),
    ]
