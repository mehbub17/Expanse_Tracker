# Generated by Django 5.0.6 on 2024-07-19 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_requestslogs'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestslogs',
            name='request_method',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]