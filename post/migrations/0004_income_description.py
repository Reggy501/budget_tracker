# Generated by Django 5.1.4 on 2024-12-17 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_expense_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
