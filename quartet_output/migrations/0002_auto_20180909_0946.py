# Generated by Django 2.0.5 on 2018-09-09 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quartet_output', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='epcisoutputcriteria',
            name='receiver_identifier',
            field=models.CharField(help_text='Typically an SGLN but an identifier that is in the SBDH and uniquely identifies a receiving entity.', max_length=250, null=True, verbose_name='SBDH Receiver Identifier'),
        ),
        migrations.AddField(
            model_name='epcisoutputcriteria',
            name='sender_identifier',
            field=models.CharField(help_text='Typically an SGLN but an identifier that is in the SBDH and uniquely identifies a sending entity.', max_length=250, null=True, verbose_name='SBDH Sender Identifier'),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='name',
            field=models.CharField(help_text='The name of the endpoint', max_length=150, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='epcisoutputcriteria',
            name='name',
            field=models.CharField(help_text='The name of the criteria record', max_length=150, unique=True, verbose_name='Name'),
        ),
    ]
