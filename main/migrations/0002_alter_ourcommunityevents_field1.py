# Generated by Django 4.2.4 on 2023-08-30 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ourcommunityevents',
            name='field1',
            field=models.CharField(max_length=100),
        ),
    ]
