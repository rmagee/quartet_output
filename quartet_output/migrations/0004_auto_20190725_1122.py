# Generated by Django 2.0.5 on 2019-07-25 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quartet_output', '0003_auto_20190214_1806'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authenticationinfo',
            options={'ordering': ['username'], 'verbose_name': 'Authentication Info', 'verbose_name_plural': 'Authentication Info'},
        ),
        migrations.AlterModelOptions(
            name='endpoint',
            options={'ordering': ['name'], 'verbose_name': 'End Point', 'verbose_name_plural': 'End Points'},
        ),
        migrations.AlterModelOptions(
            name='epcisoutputcriteria',
            options={'ordering': ['name'], 'verbose_name': 'EPCIS Output Criteria', 'verbose_name_plural': 'EPCIS Output Criteria'},
        ),
    ]
