# Generated by Django 2.1.3 on 2019-03-09 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_auto_20190309_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopinvoice',
            name='authority',
            field=models.CharField(blank=True, max_length=127, null=True),
        ),
        migrations.AlterField(
            model_name='workshopinvoice',
            name='logs',
            field=models.CharField(blank=True, max_length=127, null=True),
        ),
        migrations.AlterField(
            model_name='workshopinvoice',
            name='ref_id',
            field=models.CharField(blank=True, max_length=127, null=True),
        ),
    ]
