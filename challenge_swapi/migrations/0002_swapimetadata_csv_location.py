# Generated by Django 4.1.5 on 2023-02-01 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge_swapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='swapimetadata',
            name='csv_location',
            field=models.CharField(default=1, max_length=166),
            preserve_default=False,
        ),
    ]
