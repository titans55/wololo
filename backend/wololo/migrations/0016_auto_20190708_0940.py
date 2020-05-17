# Generated by Django 2.2.2 on 2019-07-08 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wololo', '0015_auto_20190601_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='villagetroops',
            name='total_troops_quantity_json',
        ),
        migrations.AlterField(
            model_name='villagetroops',
            name='village_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='village_troops', to='wololo.Villages'),
        ),
    ]
