# Generated by Django 2.2.2 on 2019-07-08 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wololo', '0020_reports_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='battleresults',
            name='result',
            field=models.CharField(choices=[('won', 'Won'), ('draw', 'Draw'), ('lost', 'Lost')], default='won', max_length=5),
            preserve_default=False,
        ),
    ]