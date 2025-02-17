# Generated by Django 5.1.2 on 2025-01-08 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_rename_username_cartitem_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='added_on',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='book_copy',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='item_type',
            field=models.CharField(choices=[('book', 'Book')], default='book', max_length=10),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='requested_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
