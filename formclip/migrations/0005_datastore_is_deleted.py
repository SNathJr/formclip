# Generated by Django 3.1.5 on 2021-01-16 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formclip', '0004_datastore_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='datastore',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
