# Generated by Django 3.2.25 on 2024-06-30 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('q1bapp', '0008_alter_patient_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.CharField(blank=True, max_length=343, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='pateint_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='q1bapp.patient'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='treatment',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
