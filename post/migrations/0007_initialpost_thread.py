# Generated by Django 3.2.18 on 2023-03-09 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_initial'),
        ('post', '0006_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='initialpost',
            name='thread',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='forum.thread'),
        ),
    ]
