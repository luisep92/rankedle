# Generated by Django 5.1.5 on 2025-01-26 23:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SongManager', '0013_alter_mapdifficulty_stars'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='User Name')),
            ],
        ),
        migrations.AlterField(
            model_name='mapdifficulty',
            name='stars',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Stars'),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='SongManager.map')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='SongManager.user')),
            ],
        ),
    ]
