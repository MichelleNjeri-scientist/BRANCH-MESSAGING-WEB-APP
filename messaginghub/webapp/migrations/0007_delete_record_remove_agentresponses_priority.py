# Generated by Django 4.2.6 on 2023-10-23 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_alter_agentresponses_message_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Record',
        ),
        migrations.RemoveField(
            model_name='agentresponses',
            name='priority',
        ),
    ]
