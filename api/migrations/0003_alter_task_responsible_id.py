# Generated by Django 3.2.4 on 2021-06-17 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_user_id_employe_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='responsible_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.responsible'),
        ),
    ]
