# Generated by Django 4.1.5 on 2023-02-01 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge_swapi', '0003_alter_swapimetadata_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swapimetadata',
            name='date',
            field=models.CharField(max_length=120),
        ),
    ]
