# Generated by Django 4.2 on 2024-10-09 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_alter_event_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='media_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]