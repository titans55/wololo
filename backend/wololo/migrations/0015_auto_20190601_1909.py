# Generated by Django 2.1.7 on 2019-06-01 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wololo', '0014_auto_20190601_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upgradingdetails',
            name='task_id',
            field=models.CharField(max_length=100),
        ),
    ]