# Generated by Django 3.0.7 on 2020-10-13 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20201013_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]