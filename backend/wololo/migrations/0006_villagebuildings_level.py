# Generated by Django 2.1.5 on 2019-04-23 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wololo', '0005_auto_20190423_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='villagebuildings',
            name='level',
            field=models.PositiveIntegerField(default=0),
        ),
    ]