# Generated by Django 4.1.3 on 2023-03-04 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_key_words_event_information'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event_statistics',
            name='event_id',
        ),
        migrations.DeleteModel(
            name='attitude_statistics',
        ),
        migrations.DeleteModel(
            name='event_statistics',
        ),
    ]
