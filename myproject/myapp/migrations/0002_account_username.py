# Generated by Django 4.0.1 on 2022-01-12 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='username',
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]