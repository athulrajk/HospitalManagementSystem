# Generated by Django 3.2.25 on 2024-06-30 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('q1bapp', '0010_rename_pateint_id_event_patient_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Event',
            new_name='Eventappointment',
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
    ]