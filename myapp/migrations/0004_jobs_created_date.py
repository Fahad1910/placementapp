# Generated by Django 5.0.3 on 2024-04-01 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_studentpofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
